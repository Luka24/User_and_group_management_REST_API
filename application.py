from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return f"{self.name} ({self.email})"


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return 'Hello!'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'name': user.name, 'email': user.email, 'group_id': user.group_id}
        output.append(user_data)
    return {"users": output}

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return {"id": user.id, "name": user.name, "email": user.email, "group_id": user.group_id}

@app.route('/users', methods=['POST'])
def add_user():
    user = User(name=request.json['name'],
                email=request.json['email'],
                group_id=request.json.get('group_id'))
    db.session.add(user)
    db.session.commit()
    return {'id': user.id}


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    user.group_id = request.json.get('group_id', user.group_id)
    db.session.commit()
    return {"message": "updated"}


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "deleted"}

@app.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    output = []
    for group in groups:
        group_data = {'id': group.id, 'name': group.name, 'description': group.description}
        output.append(group_data)
    return {"groups": output}


@app.route('/groups/<id>', methods=['GET'])
def get_group(id):
    group = Group.query.get_or_404(id)
    return dict(id=group.id, name=group.name)

@app.route('/groups', methods=['POST'])
def add_group():
    group = Group(name=request.json['name'],
    description=request.json.get('description'))
    db.session.add(group)
    db.session.commit()
    return {'id': group.id}

@app.route('/groups/<id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)
    group.name = request.json.get('name', group.name)
    group.description = request.json.get('description', group.description)
    db.session.commit()
    return {"message": "updated"}

@app.route('/groups/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    db.session.delete(group)
    db.session.commit()
    return {"message": "deleted"}

#if name == 'main':
#app.run(debug=True)