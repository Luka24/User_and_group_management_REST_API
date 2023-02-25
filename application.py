from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return f"{self.name}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref='users')

    def __repr__(self):
        return f"{self.name} ({self.email})"

@app.route('/')
def index():
    return 'Welcome to a user and group management REST API service!'

@app.route('/groups')
def get_groups():
    groups = Group.query.all()
    output = []
    for group in groups:
        group_data = {'id': group.id, 'name': group.name}
        user_data = []
        for user in group.users:
            user_data.append({'email': user.email, 'name': user.name})
        group_data['users'] = user_data
        output.append(group_data)
    return {"groups": output}


@app.route('/groups/<id>')
def get_group(id):
    group = Group.query.get_or_404(id)
    group_data = {'id': group.id, 'name': group.name}
    user_data = []
    for user in group.users:
        user_data.append({'email': user.email, 'name': user.name})
    group_data['users'] = user_data
    return group_data

@app.route('/groups', methods=['POST'])
def add_group():
    if 'name' not in request.json or not request.json['name']:
        return {"error": "name field is required"}, 400

    group = Group(name=request.json['name'])
    db.session.add(group)
    db.session.commit()
    return {'id': group.id}

@app.route('/groups/<id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)
    if group is None:
        return {"error": "not found"}
    group.name = request.json.get('name', group.name)
    db.session.commit()
    return {"message": "updated"}

@app.route('/groups/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    if group is None:
        return {"error": "not found"}
    db.session.delete(group)
    db.session.commit()
    return {"message": "deleted"}

@app.route('/users')
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'email': user.email, 'password': user.password, 'name': user.name, 'group_id': user.group_id}
        output.append(user_data)
    return {"users": output}


@app.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return {"name": user.name, "email": user.email, "group": user.group.name if user.group else None}


@app.route('/users', methods=['POST'])
def add_user():
    required_fields = ['email', 'password', 'name']
    for field in required_fields:
        if field not in request.json or not request.json[field]:
            return {"error": f"{field} field is required"}, 400

    if 'group_id' in request.json:
        group = Group.query.get(request.json['group_id'])
        if group is None:
            return {"error": "invalid group_id"}, 400
    user = User(email=request.json['email'], password=request.json['password'], name=request.json['name'], group_id=request.json.get('group_id'))
    db.session.add(user)
    db.session.commit()
    return {'id': user.id}

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user is None:
        return {"error": "not found"}

    try:
        user.email = request.json.get('email', user.email)
        user.password = request.json.get('password', user.password)
        user.name = request.json.get('name', user.name)
        user.group_id = request.json.get('group_id', user.group_id)
        db.session.commit()
        return {"message": "updated"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return {"error": "not found"}
    db.session.delete(user)
    db.session.commit()
    return {"message": "deleted"}

if __name__ == '__main__':
    app.run(debug=True)
