"""Hiking Trails."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session, json
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trail, Park
from flask_sqlalchemy import SQLAlchemy
from yelp import get_yelp_reviews
from weather import weather_forecast

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """homepage"""

    return render_template("homepage.html")


@app.route('/.json')
def weather():
    """Shows icon of weather conditions for each city in the bay area"""

    forecast = weather_forecast()
    print forecast
    weather = json.dumps(forecast)
    print weather

    return weather


# @app.route('/users')
# def user_list():
#     """Show list of users"""

#     users = User.query.all()
#     return render_template("/user_list.html", users=users)


@app.route('/register')
def registration_form():
    """Show registration form"""

    return render_template("registration_form.html")


@app.route('/register', methods=['POST'])
def register_new_user():
    """Register a new user."""

    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    new_user = User(email=email, password=password, first_name=first_name,
                    last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)

    return render_template("/profile", user=new_user)


@app.route('/login')
def log_in_form():
    """Show log_in form."""

    return render_template("log_in.html")


@app.route('/login', methods=['POST'])
def log_into_account():
    """Log into account."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Please try again or register for an account")
        return redirect("/login")

    if user.password != password:
        flash("Your password was incorrect, please try again")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You have successfully logged in!")
    return render_template("profile.html", user=user)


@app.route('/logout')
def log_out():
    """Allows user to log out of account."""

    del session["user_id"]
    flash("You are now logged out")
    return redirect("/")  # Can we keep them on the same page?


@app.route('/search')
def search_for_hikes():
    """Allows a user to search for hikes."""

    return render_template("search_form.html")


@app.route('/search-results')
def search_results():
    """Returns relevant hikes from user search."""

    # takes in parameters from search form
    # queries database for parameters
    # returns relevant results
    business_id = Trail.query.get(trail_name)

    reviews = get_yelp_reviews(business_id)
    yelp_info = json.dumps(reviews)

    return render_template("search_results.html", yelp_info=yelp_info)


@app.route('/trail')
def trail_list():
    """See a list of all trails."""

    trails = Trail.query.order_by("trail_name asc").distinct().all()
    return render_template("trail_list.html", trails=trails)


@app.route('/trail/<int:trail_id>')
def trail_details(trail_id):
    """See details for a chosen trail"""

    trail = Trail.query.get(trail_id)

    # select yelp_id from parks join trails on trails.park_name = parks.park_name where trail_id = 580 limit 1;

    trail_reviews = get_yelp_reviews("twin-peaks-san-francisco")
    yelp_reviews = json.dumps(trail_reviews)

    return render_template("trail.html", trail=trail, yelp_reviews=yelp_reviews)


@app.route('/park')
def park_list():
    """See a list of all parks."""

    parks = Park.query.order_by("park_name asc").distinct().all()
    return render_template("park_list.html", parks=parks)


@app.route('/park/<int:park_id>')
def park_description(park_id):
    """See details for a chosen trail"""

    park = Park.query.get(park_id)

    park_reviews = get_yelp_reviews("twin-peaks-san-francisco")
    yelp_reviews = json.dumps(park_reviews)

    return render_template("park.html", park=park, yelp_reviews=yelp_reviews)


################################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
