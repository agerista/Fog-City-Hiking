"""Models and database functions for Hiking Web App project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of hiking app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(75))
    password = db.Column(db.String(75))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))


class Hikes(db.Model):
    """List of hikes a user has done or would like to do."""

    __tablename__ = "hikes"

    hike_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trails_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    comment = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(10), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    temperature = db.Column(db.Integer(3), nullable=True)
    condition = db.Colum(db.String(40), nullable=True)


class Trails(db.Model):
    """List of available hiking trails."""

    __tablename__ = "trails"

    trail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trail_name = db.Column(db.String(50))
    park_id = db.Column(db.Integer, db.ForeignKey("parks.parks_id"))
    description = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(200), nullable=True)  
    duration = db.Column(db.String(50), nullable=True)
    length = db.Column(db.Float)  
    intensity = db.Column(db.String(20))


class Parks(db.Model):
    """List of parks that have hiking trails."""

    __tablename__ = "parks"

    park_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_name = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(50))
    state = db.Column(db.String(30))
    average_temp = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(500))
    yelp_id = db.Column(30)


##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hikes'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if you run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
