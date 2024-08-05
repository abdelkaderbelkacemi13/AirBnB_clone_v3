import unittest
from flask import Flask
import flake8.api.legacy as flake8
import json
from models import storage
from models.state import State
from api.v1.views import app_views
import unnittest

class TestStateAPI(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and initialize test variables."""
        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)
        self.client = self.app.test_client
        self.app.config['TESTING'] = True

        # Create some test data
        self.state1 = State(name="California")
        self.state2 = State(name="Texas")
        storage.new(self.state1)
        storage.new(self.state2)
        storage.save()

    def tearDown(self):
        """Tear down test data and clean up."""
        storage.delete(self.state1)
        storage.delete(self.state2)
        storage.save()

    def test_get_states(self):
        """Test retrieving all states."""
        res = self.client().get('/states')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 2)

    def test_get_state(self):
        """Test retrieving a single state by ID."""
        state_id = self.state1.id
        res = self.client().get(f'/states/{state_id}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['name'], "California")

    def test_create_state(self):
        """Test creating a new state."""
        res = self.client().post('/states', json={'name': 'New York'})
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['name'], 'New York')

    def test_create_state_missing_name(self):
        """Test creating a new state with missing name."""
        res = self.client().post('/states', json={})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data['description'], 'Missing Name')

    def test_update_state(self):
        """Test updating an existing state."""
        state_id = self.state1.id
        res = self.client().put(f'/states/{state_id}', json={'name': 'Nevada'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['name'], 'Nevada')

    def test_delete_state(self):
        """Test deleting a state."""
        state_id = self.state1.id
        res = self.client().delete(f'/states/{state_id}')
        self.assertEqual(res.status_code, 200)
        res = self.client().get(f'/states/{state_id}')
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()

