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
        """Test homepage"""

        result = self.client.get('/')
        self.assertIn("Welcome to Fog City Hiking", result.data)

    def test_register(self):
        """Test register page"""

        result = self.client.get('/register')
        self.assertIn("Please sign up for an account", result.data)

    def test_trail_list(self):
        """Test trail list page"""

        result = self.client.get('/trail')
        self.assertIn("All available trails in the Bay Area", result.data)

    def test_trail_details(self):
        """Test trail details page"""

        result = self.client.get('/trail/36')
        self.assertIn("Alston Park", result.data)

    def test_park_list(self):
        """Test park list page"""

        result = self.client.get('/park')
        self.assertIn("All available parks in the Bay Area", result.data)

    def test_park_details(self):
        """Test park details page"""

        result = self.client.get('/park/34')
        self.assertIn("Alston Park", result.data)

    def test_search_for_hikes(self):
        """Test search page"""

        result = self.client.get('/search')
        self.assertIn("Enter Search Parameters Below:", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()


class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'nbryant0@mapy.cz', 'password': 'abc123'},
                            follow_redirects=True
                            )
            self.assertEqual(session['user_id'], 'nbryant@mapy.cz')
            self.assertIn("You have successfully logged in!", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('You are now logged out', result.data)



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
