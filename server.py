"""Hiking Trails."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
# from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trail, Park, Hike, Attributes
from yelp import get_yelp_reviews, yelp_information
from weather import weather_forecast
from passlib.hash import argon2

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
    print email
    verification = request.form["verify-password"]
    print verification
    password = request.form["password"]
    print password
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]

    if password != verification:

        flash("Passwords do not match")
        return redirect("/register")

    else:

        hashed = argon2.hash(password)

        number = db.session.query(User.user_id).order_by(User.user_id.desc()).first()
        new = number[0]
        new_id = new + 1

        new_user = User(user_id=new_id, email=email, password=hashed, first_name=first_name,
                        last_name=last_name)

        db.session.add(new_user)
    db.session.commit()

    flash("User %s added" % email)

    hike_log = [{"trail_name": "No hikes saved yet!", "comment": ""}]

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
    hiker = db.session.query(User.user_id).filter(User.email == email).first()

    if not user:
        flash("Please try again or register for an account")
        return redirect("/login")

    if user.password != password:
        flash("Your password was incorrect, please try again")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You have successfully logged in!")

    hikes = db.session.query(Trail.trail_name, Hike.comment, Hike.user_id)\
        .join(Hike).filter_by(user_id=hiker).all()

    hike_log = []

    for hike in hikes:

        hike = {}
        trail_name = hikes[0][0]
        hike["trail_name"] = trail_name

        comment = hikes[0][1]
        hike["comment"] = comment

        hike_log.append(hike)

    return render_template("profile.html", user=user, hike_log=hike_log)


@app.route('/profile')
def profile_page():
    """Direct route to users profile page"""

    active = session['user_id']

    if active:

        current = db.session.query(User).filter(User.user_id == active)
        user = current[0]
        hike_log = db.session.query(Hike).filter(Hike.user_id == active)

    return render_template("profile.html", user=user, hike_log=hike_log)


@app.route('/logout')
def log_out():
    """Allows user to log out of account."""

    del session["user_id"]
    flash("You are now logged out")

    return redirect("/")  # to-do: can we keep them on the same page?


@app.route('/search', methods=['GET'])
def search_for_hikes():
    """Empty search form"""

    results = None

    return render_template("search_form.html", results=results)


@app.route('/search', methods=["POST"])
def results_from_search():
    """Allows a user to search for hikes."""

    trail = request.form.get("trail")
    parking = request.form.get("parking")
    restrooms = request.form.get("restroom")
    print trail, parking, restrooms
    # if trail or parking or restrooms:

    if trail:
        tr = Trail.query.join(Attributes).filter(Trail.trail_name.like('%trail%'))
        print tr.all()

    if parking == "yes":
        tr = Trail.query.join(Attributes).filter(Trail.trail_name.like('%trail%'),
            Attributes.parking == True)
        print tr.all()

    if restrooms == "yes":
        tr = Trail.query.join(Attributes, Park).filter(Trail.trail_name.like('%trail%'),
            Attributes.parking == True, Attributes.restrooms == True)
        print tr.all()
        # trails = Trail.query.join(Attributes).filter(Trail.trail_name.like('%trail%')).filter(Attributes.parking == True).filter(Attributes.restrooms == True)
    else:
        trails = Trail.query.filter(Trail.park_name != None).order_by("trail_name asc").distinct()

    search_results = tr.all()

    results = []

    for result in search_results:

        match = {}

        #to-do: get business id for each trail to use for yelp call

        trail_id = result.trail_id
        business = db.session.query(Park.yelp_id).filter(Park.park_name == Trail.park_name).first()  # this is slow, optomize for better runtime
        business_id = business[0]
        print business_id
        info = yelp_information(business_id)
        print info
        match["trail_id"] = trail_id
        match["trail_name"] = result.trail_name
        match["description"] = result.description
        match["image_url"] = info['image_url']
        match["photo"] = info['photos']
        match["open_now"] = info['open_now']
        match["open"] = info['opens']
        match["closes"] = info['closes']
        match["rating"] = info['rating']

        results.append(match)

    trail = request.form.get("trail_id")
    completed = request.form.get("completed")
    bookmark = request.form.get("bookmark")
    date_completed = request.form.get("date-completed")
    temperature = request.form.get("temperature")
    condition = request.form.get("condition")
    comment = request.form.get("comment")
    rating = request.form.get("rating")

    if completed or bookmark or date_completed or temperature or condition or comment or rating:

        trail_id = trail

        if session['user_id']:

            hiker = db.session.query(Hike.hike_id).order_by(Hike.hike_id.desc()).first()
            new = hiker[0]
            new_hiker = new + 1

            new_log = User(user_id=new_hiker, trail_id=trail_id, completed=completed,
                           date=date_completed, temperature=temperature, condition=condition,
                           comment=comment, rating=rating)

            print new_log

        else:
            flash("Please log in to continue")

    return render_template("search_form.html", results=results)  # , trail_reviews=trail_reviews


@app.route('/trail')
def trail_list():
    """See a list of all trails."""

    trails = Trail.query.filter(Trail.park_name != None).order_by("trail_name asc").distinct().all()
    return render_template("trail_list.html", trails=trails)


@app.route('/trail/<int:trail_id>')
def trail_details(trail_id):
    """See details for a chosen trail"""

    trail = Trail.query.get(trail_id)
    trail_id = trail.trail_id

    business = db.session.query(Park.yelp_id).filter(Trail.park_name == Park.park_name).filter(Trail.trail_id == trail_id).first()
    business_id = business[0]

    trail_reviews = get_yelp_reviews(business_id)

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
    park_id = park.park_id

    business = db.session.query(Park.yelp_id).filter(Park.park_id == park_id).first()
    business_id = business[0]

    park_reviews = get_yelp_reviews(business_id)

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
