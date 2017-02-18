from sqlalchemy import *
from model import Park, Trail
from transit import trips, maps, photos, attributes, trailheads


def seed_trail_table():
    """Information for trail table"""
    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']
        trail_name = trail['name']
        park_name = trail['park_name']

        print trail_id, trail_name

        trail = Trail.query.get(trail_id)

        if trail is None:

            new_trail = Trail(trail_id=trail_id,
                              trail_name=trail_name,
                              park_name=park_name)

            db.session.add(new_trail)

    db.session.commit()


def add_maps():
    """Add maps to trail table"""

    trails = trailheads()

    for trail in trails:

        trail_id = trail['id']
        map_data = maps(trail['id'])

        if map_data != []:
            map_link = map_data.pop()
            map_url = map_link['url']
            print trail_id, map_url

            trail = Trail.query.get(trail_id)

            if trail is not None and map_url is not "":

                db.session.query(Trail).filter(trail_id == trail_id).update({"maps": map_url})
                db.session.commit()


def add_images():
    """Add images to trail table"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']

        image_data = photos(trail['id'])

        if image_data != []:
            image_url = image_data.pop()
            image = image_url['flickr_url']

            trail = Trail.query.get(trail_id)

            if trail is not None:

                db.session.query(Trail).filter(trail_id == trail_id).update({"image": image})
                db.session.commit()


def add_trips():
    """Add trips to trail table"""

    trips = trips()

    for trip in trips:

        trail_id = trail['id']
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



def seed_park_table():
    """Data for park table"""

    parks = trailheads()

    for park in parks:
        trail_id = park['id']
        latitude = park['latitude']
        longitude = park['longitude']

        description = park['description']
        park_name = park['park_name']

        image_data = photos(park['id'])

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
    get_business_ids()
