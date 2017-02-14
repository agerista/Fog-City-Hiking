from sqlalchemy import *
from model import *
from server import app
from transit import *


# def seed_trail_table():
#     """Information for trail table"""
#     trails = trailheads()

#     for trail in trails:
#         trail_id = trail['id']
#         trail_name = trail['name']

#         print trail_id, trail_name

#         trail = Trail.query.get(trail_id)

#         if trail is not None:

#             new_trail = Trail(trail_id=trail_id,
#                               trail_name=trail_name)

#             db.session.add(new_trail)

#     db.session.commit()


def add_maps():
    """Add maps to trail table"""

    trails = trailheads()

    for trail in trails:

        map_data = maps(trail['id'])
        trail_id = trail['id']

        if map_data == []:
            map_url = None
            print map_url
        else:
            map_link = map_data.pop()
            map_url = map_link['url']
            print map_url

        trail = Trail.query.get(trail_id)

        if trail is not None:

            new_map = Trail(maps=map_url)

            db.session.add(new_map)

    db.session.commit()


def add_images():
    """Add images to trail table"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']

        image_data = photos(trail['id'])

        if image_data == []:
            image = None
            print image

        elif image_data is not None:
            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']
                print image

            except:
                pass

        trail = Trail.query.get(trail_id)

        if trail is not None:

            new_image = Trail(image=image)

            db.session.add(new_image)

    db.session.commit()


def add_trips():
    """Add trips to trail table"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']

    trip = trips(trail['id'])

    if trip:
        length = trip['length_miles']
        duration = trip['duration']
        intensity = trip["intensity"]

        print length, intensity, duration

    else:
        length = None
        duration = None
        intensity = None

        print length, intensity, duration

    trail = Trail.query.get(trail_id)

    if trail is not None:

        new_trip = Trail(length=length,
                         duration=duration,
                         intensity=intensity)

        db.session.add(new_trip)

    db.session.commit()


# def seed_park_table():
#     """Data for park table"""

#     parks = trailheads()

#     for park in parks:
#         trail_id = park['id']
#         latitude = park['latitude']
#         longitude = park['longitude']

#         description = park['description']
#         park_name = park['park_name']

#         image_data = photos(park['id'])

#         if image_data != []:
#             image_url = image_data.pop()
#             image = image_url['flickr_url']

#         else:
#             image = None

#         print image

#         park = Park(latitude=latitude,
#                     longitude=longitude,
#                     description=description,
#                     park_name=park_name,
#                     image=image)

#         db.session.add(park)

#     db.session.commit()
#     print "done committing parks"

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # seed_park_table()
    # seed_trail_table()
    add_maps()
    add_images()
    add_trips()
