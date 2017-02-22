"""Hiking Trails."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session, json
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trail, Park, Hike, Attributes
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
    # weather = json.dumps(forecast)
    # print weather

    return jsonify(forecast)


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

    number = db.session.query(User.user_id).order_by(User.user_id.desc()).first()
    new = number[0]
    new_id = new + 1

    new_user = User(user_id=new_id, email=email, password=password, first_name=first_name,
                    last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)

    hike_log = ["No hikes saved yet!"]

    return render_template("profile.html", user=new_user, hike_log=hike_log)


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
    hike_log = db.session.query(Trail.trail_name, Hike.comment, Hike.user_id)\
        .join(Hike).filter_by(user_id=1).all()

    if not user:
        flash("Please try again or register for an account")
        return redirect("/login")

    if user.password != password:
        flash("Your password was incorrect, please try again")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You have successfully logged in!")

    # if  hike:
    #     trail_name = Trail.trail_name
    #     comment = Hike.comment

    return render_template("profile.html", user=user, hike_log=hike_log)


@app.route('/logout')
def log_out():
    """Allows user to log out of account."""

    del session["user_id"]
    flash("You are now logged out")
    return redirect("/")  # to-do: can we keep them on the same page?


@app.route('/search', methods=["GET", "POST"])
def search_for_hikes():
    """Allows a user to search for hikes."""

    trail_name = request.form.get("ocean")
    parking = request.form.get("parking")
    restrooms = request.form.get("restrooms")
    # duration = request.form.get("duration")
    print trail_name, restrooms, parking

    if trail_name is not None:
        trail = Trail.query.join(Attributes).filter(Trail.trail_name.like('%trail_name%'))
        print trail

    if parking == "yes":
        trail = Trail.query.join(Attributes).filter(Trail.trail_name.like('%park%')).filter(Attributes.parking == True)
        print trail

    if restrooms == "yes":
        trail = Trail.query.join(Attributes).filter(Trail.trail_name.like('%park%')).filter(Attributes.parking == True).filter(Attributes.restrooms == True)
        print trail

    results = trail.all()
    print results

    return render_template("search_form.html", results=results)  # , trail_reviews=trail_reviews


# @app.route('/search-results')
# def search_results():
#     """Returns relevant hikes from user search."""

    # takes in parameters from search form
    # queries database for parameters
    # returns relevant results

    # select yelp_id from parks join trails on trails.park_name = parks.park_name where trail_name = 'Panoramic Trail';
    # business_id = db.session.query(Park.yelp_id).join(Trail).filter(Trail.trail_name.like('%trail%'))
    # trail_reviews = get_yelp_reviews(business_id)



    # return render_template("search-results.html")


@app.route('/trail')
def trail_list():
    """See a list of all trails."""

    trails = Trail.query.filter(Trail.park_name != None).order_by("trail_name asc").distinct().all()
    return render_template("trail_list.html", trails=trails)


@app.route('/trail/<int:trail_id>')
def trail_details(trail_id):
    """See details for a chosen trail"""

    trail = Trail.query.get(trail_id)

    # select yelp_id from parks join trails on trails.park_name = parks.park_name where trail_id = 580 limit 1;

    trail_reviews = get_yelp_reviews("twin-peaks-san-francisco")

    print trail_reviews

    return render_template("trail.html", trail=trail, trail_reviews=trail_reviews)


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

    return render_template("park.html", park=park, park_reviews=park_reviews)


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
