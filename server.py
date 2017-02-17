"""Hiking Trails."""

import requests
import os
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session, json
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trail, Park, Hike
from flask_sqlalchemy import SQLAlchemy
from yelp import get_header, obtain_bearer_token, get_yelp_reviews, yelp_information
from weather import weather_forecast
import forecastio

api_key = os.environ["DARK_KEY"]


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def weather_forecast():
    """Get the weather"""

    # Cap is 1,000 calls per day
    # db.session.query(Park.latitude, Park.longitude).filter_by(city).distinct().all()
    coordinates = [(37.7749, -122.4194), (37.8044, -122.2711), (37.8716, -122.2727), (38.0834, -122.7633), (37.6138, -122.4869)]
    info = []
    weather_info = []

    for coordinate in coordinates:

        lat = coordinate[0]
        info.append(lat)
        lng = coordinate[1]
        info.append(lng)

        weather = forecastio.load_forecast(api_key, lat, lng)

        hour = weather.hourly()
        summary = hour.summary
        info.append(summary)

        icon = hour.icon
        info.append(icon)

        weather_info.append(info)
        print weather_info


    return render_template("homepage.html")


@app.route('/.json')
def weather_info():
    """JSON info about the weather"""

    return jsonify(weather)


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("/user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_profile_page(user_id):
    """Shows the users profile page"""

    user = User.query.get(user_id)

    return render_template("user.html", user=user)


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

    return redirect("/")


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
    return redirect("/users/%s" % user.user_id)


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
    trail = Trail.query.get(trail_name)
    reviews = get_yelp_reviews("twin-peaks-san-francisco")
    yelp_info = json.loads(reviews)
    print yelp_info

    return render_template("search_results.html")


@app.route('/trail')
def trail_list():
    """See a list of all trails."""

    trails = Trail.query.order_by("trail_name asc").distinct().all()
    return render_template("trail_list.html", trails=trails)

@app.route('/trail/<int:trail_id>')
def trail_details(trail_id):
    """See details for a chosen trail"""

    trail = Trail.query.get(trail_id)

    trail_reviews = get_yelp_reviews("twin-peaks-san-francisco")

    yelp_reviews = json.dumps(trail_reviews)

    return render_template("trail.html", trail=trail, yelp_reviews=yelp_reviews)


# @app.route('/trail/<int:trail_id>')
# def trail_details(trail_id):
#     """See details for a chosen trail."""

#     trail = Trail.query.get(trail_id)

#     # select yelp_id from parks join trails on trails.park_name = parks.park_name where trail_id = 580 limit 1;
#     # business_id = db.session.query(Park).join(Trail).filter_by(trail_id=trail).first()

#     return render_template("trail.html", trail=trail)


@app.route('/park')
def park_list():
    """See a list of all parks."""

    parks = Park.query.order_by("park_name asc").distinct().all()
    return render_template("park_list.html", parks=parks)


@app.route('/park/<int:park_id>')
def park_description(park_id):
    """See details for a chosen trail"""

    park = Park.query.get("park_id")

    return render_template("park.html", park=park)




################################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
