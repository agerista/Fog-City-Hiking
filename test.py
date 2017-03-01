from unittest import TestCase
from model import connect_to_db, db, example_data,  User, Park, Hike, Trail
from flask import session
from server import app


class FlaskTests(TestCase):
    def setUp(self):
        """Do this before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show errors that happen during Tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///test")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_index(self):

        result = self.client.get('/')
        self.assertIn("Welcome to Fog City Hiking", result.data)

    def test_trail_list(self):

        result = self.client.get('/trail')
        self.assertIn("All available trails in the Bay Area", result.data)

    def test_park_list(self):

        result = self.client.get('/park')
        self.assertIn("All available parks in the Bay Area", result.data)

    def test_search_for_hikes(self):

        result = self.client.get('/search')
        self.assertIn("Enter Search Parameters Below:", result.data)


class FlaskTestsDatabases(TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///test")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_find_trail(self):
        """Can we find a trail in the sample data?"""

        alston_trail = Trail.query.filter(Trail.trail_name == "Alston Park").first()
        self.assertEqual(alston_trail.trail_name, "Alston Park")

    def test_find_park(self):
        """Can we find a park in the sample data?"""

        angel_island = Park.query.filter(Park.park_name == "Angel Island State Park").first()
        self.assertEqual(angel_island.park_name, "Angel Island State Park")

    def test_find_user(self):
        """Can we find a user in the sample data?"""

        nancy = User.query.filter(User.first_name == "Nancy").first()
        self.assertEqual(nancy.first_name, "Nancy")

    def test_find_hike(self):
        """Can we find a hike in the sample data?"""

        consequat = Hike.query.filter(Hike.comment == "consequat").first()
        self.assertEqual(consequat.comment, "consequat")


################################################################################
if __name__ == "__main__":

    import unittest

    unittest.main()
