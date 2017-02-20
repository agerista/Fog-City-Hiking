"""Utility - seeds tables. Transitandtrails and Yelp APIs"""

from sqlalchemy import func
from model import connect_to_db, db
from model import Park, Trail, Attributes, User
from transit import maps, photos, attributes, trailheads, trips


def seed_trail_table():
    """Information for trail table"""
    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']
        trail_name = trail['name']
        park_name = trail['park_name']

        trail = Trail.query.get(trail_id)

        if trail is None:

            new_trail = Trail(trail_id=trail_id,
                              trail_name=trail_name,
                              park_name=park_name)

            db.session.add(new_trail)

    db.session.commit()
    print "Done seeding trail table"


def add_maps():
    """Add maps to trail table"""

    trails = trailheads()

    for trail in trails:

        trail_id = trail['id']
        map_data = maps(trail_id)

        if map_data != []:
            map_link = map_data.pop()
            map_url = map_link['url']
            print trail_id, map_url

            trail = Trail.query.get(trail_id)

            if trail is not None and map_url is not "":

                db.session.query(Trail).filter(trail_id == trail_id).update({"maps": map_url})
                db.session.commit()
                print "Done committing maps"


def add_images():
    """Add images to trail table"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']

        image_data = photos(trail_id)

        if image_data != []:
            image_url = image_data.pop()
            image = image_url['flickr_url']

            trail = Trail.query.get(trail_id)

            if trail is not None:

                db.session.query(Trail).filter(trail_id == trail_id).update({"image": image})
                db.session.commit()
                print "done committing images"


def add_trail_id_attributes():

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']

        attribute = Attributes(trail_id=trail_id)

        db.session.add(attribute)

    db.session.commit()
    print "done with attrs"

def add_attributes():
    """Add attributes to trail"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']

        attribute_data = attributes(trail_id)
        print attribute_data

        attribute_list = attribute_data
        if attribute_list != []:

            i = 0

            while i < len(attribute_list):

                if attribute_list[i]["name"] == 'Drinking Water':
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"water": True})
                    print "water"

                if attribute_list[i]["name"] == "Restrooms":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"restrooms": True})
                    print "restrooms"

                if attribute_list[i]["name"] == "Visitor Center":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"visitor_center": True})
                    print "visit"

                if attribute_list[i]["name"] == "Parking":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"parking": True})
                    print "parking"

                if attribute_list[i]["name"] == "Birding":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"birding": True})
                    print "birding"

                if attribute_list[i]["name"] == "Picnic Tables":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"picnic_tables": True})
                    print "Picnic"

                if attribute_list[i]["name"] == "Dirt":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"dirt_path": True})
                    print "dirt"

                if attribute_list[i]["name"] == "Paved":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"paved_path": True})
                    print "paved"

                if attribute_list[i]["name"] == "Gravel":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"gravel_path": True})
                    print "gravel"

                if attribute_list[i]["name"] == "No Dogs Allowed":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"dog_free": True})
                    print "dog_free"

                if attribute_list[i]["name"] == "Dogs Allowed On-leash":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"dogs_on_leash": True})
                    print "dogs leash"

                if attribute_list[i]["name"] == "Dogs Allowed Off-leash":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"dogs_off_leash": True})
                    print "Off-leash"

                if attribute_list[i]["name"] == "Transit":
                    db.session.query(Attributes).filter(trail_id == trail_id).update({"transit_near": True})
                    print "transit"

                db.session.commit()
                i += 1

    print "done committing attributes"


def add_trips():
    """Add trips to trail table"""

    trails = trailheads()

    for t in trails:

        trail_id = trails['id']
        trip = trips()

        if trip != []:
            length = trip['length_miles']
            intensity = trip["intensity"]
            duration = trip['duration']

            description = trip["description"]
            trail_id = ['starting_trailhead_id']

            print length, intensity, duration, description, trail_id

            trail = Trail.query.get(trail_id)

            if trail is not None:

                db.session.query(Trail).filter(trail_id == trail_id).update({"length": length,
                                                                             "intensity": intensity,
                                                                             "duration": duration,
                                                                             "description": description})

                db.session.commit()
                print "Done committing trips"


def seed_park_table():
    """Data for park table"""

    parks = trailheads()

    for park in parks:
        trail_id = park['id']
        latitude = park['latitude']
        longitude = park['longitude']

        description = park['description']
        park_name = park['park_name']

        image_data = photos(trail_id)

        if image_data != []:
            image_url = image_data.pop()
            image = image_url['flickr_url']

        else:
            image = None

        print image

        park = Park(latitude=latitude,
                    longitude=longitude,
                    description=description,
                    park_name=park_name,
                    image=image)

        db.session.add(park)

    db.session.commit()
    print "done committing parks"


def add_users():
    """Seed fake users to data base"""

    for row in open("static/mock_users.csv"):
        row = row.rstrip()
        email, password, first_name, last_name = row.split(",")

        user = User(email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name)

        db.session.add(user)

    db.session.commit()

################################################################################
if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # seed_park_table()
    # seed_trail_table()
    # add_maps()
    # add_images()
    # add_trips()
    # add_attributes()
    # add_trail_id_attributes()
    add_users()
