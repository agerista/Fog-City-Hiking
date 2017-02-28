from unittest import TestCase
from model import User, Hike, Trail, Park, Attributes, connect_to_db, db, example_data
from server import app
import server


class FlaskTests(TestCase):
    def setUp(self):
        """Do this before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show errors that happen during Tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql://testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do this at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_find_trail(self):
        """Can we find a trail in the sample data?"""

        twin_peaks = Trail.query.filter(Trail.trail_name == "Alston Park").first()
        self.assertEqual('Alston Park'.trail_name, "Alston Park")

    def test_find_park(self):
        """Can we find a park in the sample data?"""

        butano = Park.query.filter(Park.park_name == "Butano State Park").first()
        self.assertEqual("Butano State Park".name, "Butano State Park")
