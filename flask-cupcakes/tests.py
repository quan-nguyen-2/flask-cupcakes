from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeRoutesTestCase(TestCase):
    """Test for routes rendering cupcake templates"""
    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_render_homepage(self):
        """Test that the '/' route renders home.html and displays new cupcake form"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('All Cupcakes', html)
            self.assertIn('Add a New Cupcake', html)

    def test_show_cupcake(self):
        """Tests that the '/cupcake/<int:cupcake_id>' route renders data for the cupcake with and id of cupcake_id"""
        with app.test_client() as client:
            resp = client.get(f'/cupcake/{self.cupcake.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFlavor', html)
        
    def test_invalid_show_cupcake(self):
        """Tests that the route returns a status code of 404 if the id does not exist in the database"""
        with app.test_client() as client:
            resp = client.get('/cupcake/123456789')
            self.assertEqual(resp.status_code, 404)



class CupcakeViewsTestCase(TestCase):
    """Tests for views of API endpoints."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_get_cupcakes(self):
        """Tests that the '/api/cupcakes' endpoint returns valid JSON data of cupcakes in the database"""
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": '5',
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_create_cupcake(self):
        """Tests that the '/api/cupcakes' route using the POST method creates a new cupcake, adds it to the database, and returns valid JSON data of the cupcake.
        Tests that the number of cupcakes in the database reflects the added cupcake."""
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # we don't know what ID we'll get, so here we make sure it's set as an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": '10',
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Tests that the '/api/cupcakes/<int:cupcake_id>' route using the POST method receives data and uses it to update the cupcake with matching ID in the database, and then returns that cupcakes updated data as valid JSON"""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.post(url, json=CUPCAKE_DATA)

            data = resp.json

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": '5',
                    "image": "http://test.com/cupcake.jpg"
                }
            })


    def test_delete_cupcake(self):
        """Tests that the '/api/cupcakes/<int:cupcake_id' route using the DELETE method successfully removes the cupcake with matching id from the database and returns a JSON message"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)
            data = resp.json
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {'message': 'Deleted'})

