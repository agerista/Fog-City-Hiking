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

    hike_log = [{"trail_name": "No hikes saved yet", "comment": ""}]


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
    hashed = argon2.hash(password)

    user = User.query.filter_by(email=email).first()
    hiker = db.session.query(User.user_id).filter(User.email == email).first()

    while True:

        if argon2.verify(password, hashed):

            session["user_id"] = user.user_id

            flash("You have successfully logged in!")

            hikes = db.session.query(Hike.comment, Hike.temperature, Hike.rating,
                Hike.date, Hike.completed, Hike.condition, Trail.trail_name,
                Trail.length, Trail.intensity).join(Trail).filter(Hike.user_id == hiker).all()

            hike_log = []

            for hike in hikes:

                log = {}

                log['comment'] = hike.comment
                log['temperature'] = hike.temperature
                log['rating'] = hike.rating
                log['date'] = hike.date
                log['completed'] = hike.completed
                log['condition'] = hike.condition
                log['trail_name'] = hike.trail_name
                log['length'] = hike.length
                log['intensity'] = hike.intensity

                hike_log.append(log)

                print hike_log

            break

        if not user:
            flash("Please try again or register for an account")
            return redirect("/login")

        if not password:
            argon2.verify(password, hashed)
            flash("Your password was incorrect, please try again")
            return redirect("/login")

    return render_template("profile.html", user=user, hike_log=hike_log)


@app.route('/profile')
def profile_page():
    """Direct route to users profile page"""

    active = session['user_id']

    if active:

        user = db.session.query(User).filter(User.user_id == active).first()

        # hike_log = db.session.query(Hike).filter(Hike.user_id == active)
        hikes = db.session.query(Hike.comment, Hike.temperature, Hike.rating,
            Hike.date, Hike.completed, Hike.condition, Trail.trail_name,
            Trail.length, Trail.intensity).join(Trail).filter(Hike.user_id == user.user_id).all()

        hike_log = []

        for hike in hikes:

            log = {}

            log['comment'] = hike.comment
            log['temperature'] = hike.temperature
            log['rating'] = hike.rating
            log['date'] = hike.date
            log['completed'] = hike.completed
            log['condition'] = hike.condition
            log['trail_name'] = hike.trail_name
            log['length'] = hike.length
            log['intensity'] = hike.intensity

            hike_log.append(log)

            print hike_log


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
    t = "%" + trail + "%"
    miles = request.form.get("length")
    intensity = request.form.get("intensity")
    inten = "%" + str(intensity) + "%"
    restrooms = request.form.get("restroom")
    parking = request.form.get("parking")
    dog_free = request.form.get("dog-free")
    on_leash = request.form.get("on-leash")
    off_leash = request.form.get("off_leash")
    city =request.form.get("city")
    c = "%" + city + "%"

    print "TRAIL, MILES", trail, miles, intensity, restrooms, parking

    if trail:
        print "in trail"
        hike = Trail.query.join(Attributes).filter(Trail.trail_name.ilike(t)).limit(5)

    elif city:
        print "in city"
        hike = Trail.query.join(Attributes).filter(Trail.park_name == Park.park_name).filter(
            Trail.trail_name.ilike(t)).filter(Park.city.ilike(c)).limit(5)

    elif miles:
        print "in miles"
        hike = Trail.query.join(Attributes).filter(Trail.park_name == Park.park_name).filter(
            Trail.length == miles, Trail.trail_name.ilike(t)).filter(Park.city.ilike(c)).limit(5)


        # hike = Trail.query.join(Attributes).filter(Trail.length == miles,
        #     Trail.trail_name.ilike(t)).limit(5)
        # print hike.all()

    elif intensity:
        print "in intensity"
        hike = Trail.query.join(Attributes).filter(Trail.intensity.ilike(inten),
            Trail.length == miles, Trail.trail_name.ilike(t)).limit(5)

    elif restrooms == "yes":
        print "in restrooms"
        hike = Trail.query.join(Attributes).filter(Trail.intensity.ilike(inten)).filter(
            Trail.trail_name.ilike(t)).filter(Attributes.restrooms == True).limit(5)
        print hike.all()

    elif parking == "yes":
        print "in parking"
        hike = Trail.query.join(Attributes).filter(Trail.intensity.ilike(inten),
            Trail.length == miles,Trail.trail_name.ilike(t)).filter(Attributes.parking
            == True, Attributes.restrooms == True).limit(5)

    elif dog_free == "yes":
        print "dog free"
        hike = Trail.query.join(Attributes).filter(Trail.intensity.ilike(inten),
            Trail.length == miles,Trail.trail_name.ilike(t)).filter(Attributes.parking
            == True, Attributes.restrooms == True, Attributes.dog_free == True).limit(5)

    elif on_leash == "yes":
        print "on_leash"
        hike = Trail.query.join(Attributes).filter(Trail.intensity.ilike(inten),
            Trail.length == miles,Trail.trail_name.ilike(t)).filter(Attributes.parking
            == True, Attributes.restrooms == True, Attributes.dogs_on_leash == True).limit(5)

    elif off_leash == "yes":
        print "off_leash"
        hike = Trail.query.join(Attributes).filter(Trail.intensity.ilike(inten),
            Trail.length == miles,Trail.trail_name.ilike(t)).filter(Attributes.parking
            == True, Attributes.restrooms == True, Attributes.dogs_off_leash == True).limit(5)

    else:
        print "in else"
        hike = Trail.query.filter(Trail.park_name != None).distinct().limit(5)  # to-do: make this a view and include all trails

    search_results = hike.all()

    results = []

    for result in search_results:

        match = {}

        trail_id = result.trail_id
        print trail_id
        # business = db.session.query(Park.yelp_id).filter(Park.park_name == Trail.park_name).first()  # this is slow, optomize for better runtime
        business = db.session.query(Park.yelp_id).filter(Park.park_name == Trail.park_name).filter(Trail.trail_id == trail_id).first()
        print business
        business_id = business[0]
        print business_id
        info = yelp_information(business_id)

        match["trail_id"] = result.trail_id
        match["trail_name"] = result.trail_name
        match["trail_image"] = result.image
        match["length"] = result.length
        match["intensity"] = result.intensity
        match["description"] = result.description
        # match["parking"] = result.parking
        match["image_url"] = info['image_url']
        match["photos"] = info['photos']
        info['photos']
        match["open_now"] = info['open_now']
        match["open"] = info['opens']
        match["closes"] = info['closes']
        match["rating"] = info['rating']

        results.append(match)

    return render_template("search_form.html", results=results, search_results=search_results)


@app.route('/save', methods=["POST"])
def save_hike_results():
    """Save hike from search form"""

    trail = request.form.get("trail_id")
    completed = request.form.get("completed")
    bookmark = request.form.get("bookmark")
    date_completed = request.form.get("date-completed")
    temperature = request.form.get("temperature")
    condition = request.form.get("condition")
    comment = request.form.get("comment")
    rating = request.form.get("rating")

    if completed or bookmark or date_completed or temperature or condition or comment or rating:
        print comment
        trail_id = trail

        if session['user_id']:
            print session['user_id']

            hiker = db.session.query(Hike.hike_id).order_by(Hike.hike_id.desc()).first()
            new = hiker[0]
            new_hiker = new + 1

            new_log = User(user_id=new_hiker, trail_id=trail_id, completed=completed,
                           date=date_completed, temperature=temperature, condition=condition,
                           comment=comment, rating=rating)

            db.session.add(new_log)
            print "added"
            db.session.commit()
            print "committed"
            print new_log

        else:
            flash("Please log in to continue")

            # to-do: window.load()? for saving search results to hike log? research.
  # , trail_reviews=trail_reviews
    return render_template("search_form.html", results=results, search_results=search_results)

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

    attr = db.session.query(Attributes).filter(Attributes.trail_id ==
                 trail_id).one()

    attributes = {}
    attribute_list = []

    attributes['water'] = attr.water
    attributes['restrooms'] = attr.restrooms
    attributes['visitor_center'] = attr.visitor_center
    attributes['parking'] = attr.parking
    attributes['birding'] = attr.birding
    attributes['picnic_tables'] = attr.picnic_tables
    attributes['dirt_path'] = attr.dirt_path
    attributes['paved_path'] = attr.paved_path
    attributes['gravel_path'] = attr.gravel_path
    attributes['dog_free'] = attr.dog_free
    attributes['dogs_off_leash'] = attr.dogs_off_leash
    attributes['dogs_on_leash'] = attr.dogs_on_leash

    for key, value in attributes.iteritems():

        if value == True:

            attribute_list.append(key)

    business = db.session.query(Park.yelp_id).filter(Trail.park_name ==
                Park.park_name).filter(Trail.trail_id == trail_id).first()
    business_id = business[0]

    trail_reviews = get_yelp_reviews(business_id)
    trail_info = yelp_information(business_id)

    return render_template("trail.html", trail=trail, trail_reviews=trail_reviews,
                           trail_info=trail_info, attribute_list=attribute_list)


@app.route('/trails-by-city')
def trail_by_city():
    """Organize trails by city for user experience"""

    trail = db.session.query(Trail.trail_name, Park.city).filter(Park.city != None).filter(
        Trail.trail_name == Park.park_name).order_by(Park.city, Trail.trail_name).distinct().all()

    trails = {}

    for t in trail:
        a = str(t[0])
        b = str(t[1])
        if b not in trails:
            trails[b] = []
            trails[b].append(a)
        else:
            trails[b].append(a)
    print trails

    return render_template("trails-by-city.html", trails=trails)


@app.route('/park')
def park_list():
    """See a list of all parks."""

    parks = Park.query.order_by("park_name asc").distinct().all()
    return render_template("park_list.html", parks=parks)


@app.route('/park/<int:park_id>')
def park_details(park_id):
    """See details for a chosen trail"""

    park = Park.query.get(park_id)
    park_id = park.park_id

    # to-do: figure out query for park attributes

    # attr = db.session.query(Attributes).filter(Attributes.trail_id ==
    #          trail_id).one()

    # attributes = {}
    # attribute_list = []

    # attributes['water'] = attr.water
    # attributes['restrooms'] = attr.restrooms
    # attributes['visitor_center'] = attr.visitor_center
    # attributes['parking'] = attr.parking
    # attributes['birding'] = attr.birding
    # attributes['picnic_tables'] = attr.picnic_tables
    # attributes['dirt_path'] = attr.dirt_path
    # attributes['paved_path'] = attr.paved_path
    # attributes['gravel_path'] = attr.gravel_path
    # attributes['dog_free'] = attr.dog_free
    # attributes['dogs_off_leash'] = attr.dogs_off_leash
    # attributes['dogs_on_leash'] = attr.dogs_on_leash

    # for key, value in attributes.iteritems():

    #     if value == True:

    #         attribute_list.append(key)

    business = db.session.query(Park.yelp_id).filter(Park.park_id == park_id).first()
    business_id = business[0]

    park_reviews = get_yelp_reviews(business_id)
    park_info = yelp_information(business_id)

    return render_template("park.html", park=park, park_reviews=park_reviews, park_info=park_info)

@app.route('/parks-by-city')
def parks_by_city():
    """Organize trail by city for user experience"""

    park = db.session.query(Park.park_name, Park.city).filter(Park.city
        != None).order_by(Park.city, Park.park_name).distinct().all()

    parks = {}

    for p in park:
        a = str(p[0])
        b = str(p[1])
        if b not in parks:
            parks[b] = []
            parks[b].append(a)
        else:
            parks[b].append(a)
    print parks

    return render_template("parks-by-city.html", parks=parks)


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
