import json
import unittest
from application import app, db, Group, User

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Called before each test."""
        self.app = app.test_client()
        # create a new in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app_context().push()
        db.create_all()

    def tearDown(self):
        """Called after each test."""
        db.session.remove()
        db.drop_all()

    def test_index_endpoint(self):
        """Test the index endpoint returns the correct message"""
        expected_response = 'Welcome to a user and group management REST API service!'
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), expected_response)

    def test_get_groups(self):
        """Test getting a list of all groups."""
        # Add some groups to the database
        group1 = Group(name='Group 1')
        group2 = Group(name='Group 2')
        db.session.add(group1)
        db.session.add(group2)
        db.session.commit()

        response = self.app.get('/groups')
        self.assertEqual(response.status_code, 200)
        groups = response.json['groups']
        self.assertEqual(len(groups), 2)

    def test_get_group(self):
        """Test getting a single group by ID."""
        group = Group(name='Test Group')
        db.session.add(group)
        db.session.commit()

        response = self.app.get(f'/groups/{group.id}')
        self.assertEqual(response.status_code, 200)
        group_data = response.json
        self.assertEqual(group_data['id'], group.id)
        self.assertEqual(group_data['name'], group.name)

    def test_update_group(self):
        """Test updating an existing group."""
        group = Group(name='Test Group')
        db.session.add(group)
        db.session.commit()

        data = {'name': 'New Group Name'}
        response = self.app.put(f'/groups/{group.id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'updated'})

        updated_group = Group.query.get(group.id)
        self.assertEqual(updated_group.name, data['name'])

    def test_delete_group(self):
        """Test deleting an existing group."""
        group = Group(name='Test Group')
        db.session.add(group)
        db.session.commit()

        response = self.app.delete(f'/groups/{group.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'deleted'})

        deleted_group = Group.query.get(group.id)
        self.assertIsNone(deleted_group)

    def test_add_user(self):
        """Test adding a new user."""
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User',
            'group_id': None,
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)

        user_id = response.json['id']
        user = User.query.get(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.password, data['password'])
        self.assertEqual(user.name, data['name'])
        self.assertIsNone(user.group_id)

    def test_get_users(self):
        user1 = User(email='test1@test.com', password='password1', name='Test User 1')
        user2 = User(email='test2@test.com', password='password2', name='Test User 2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'users': [{'email': 'test1@test.com', 'password': 'password1', 'name': 'Test User 1', 'group_id': None},
                      {'email': 'test2@test.com', 'password': 'password2', 'name': 'Test User 2', 'group_id': None}]})

    def test_get_user(self):
        # create a user for testing
        user = User(email='testuser@example.com', password='password', name='Test User')
        db.session.add(user)
        db.session.commit()

        # perform GET request
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)

        # validate response
        expected_response = {"name": "Test User", "email": "testuser@example.com", "group": None}
        self.assertEqual(response.json, expected_response)

    def test_add_user(self):
        # perform POST request
        data = {"email": "newuser@example.com", "password": "password", "name": "New User"}
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 200)

        # validate response
        self.assertEqual(response.json['id'], 1)

        # validate data was added to database
        user = User.query.filter_by(email='newuser@example.com').first()
        self.assertEqual(user.name, 'New User')
        self.assertEqual(user.group_id, None)

    def test_update_user(self):
        # create a user for testing
        user = User(email='testuser@example.com', password='password', name='Test User')
        db.session.add(user)
        db.session.commit()

        # perform PUT request
        data = {"email": "testuser@example.com", "name": "Updated Test User", "group_id": 1}
        response = self.app.put('/users/1', json=data)
        self.assertEqual(response.status_code, 200)

        # validate response
        self.assertEqual(response.json, {"message": "updated"})

        # validate data was updated in database
        user = User.query.filter_by(id=1).first()
        self.assertEqual(user.name, 'Updated Test User')
        self.assertEqual(user.group_id, 1)

    def test_delete_user(self):
        # create a user for testing
        user = User(email='testuser@example.com', password='password', name='Test User')
        db.session.add(user)
        db.session.commit()

        # perform DELETE request
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)

        # validate response
        self.assertEqual(response.json, {"message": "deleted"})

        # validate data was deleted from database
        user = User.query.filter_by(id=1).first()
        self.assertEqual(user, None)

