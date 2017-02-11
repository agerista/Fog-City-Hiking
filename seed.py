from sqlalchemy import func
from model import *
from model import connect_to_db, db
from server import app
from transit import *


def seed_trail_table():
    """Information for trail table"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']
        trail_name = trail['name']

        map_data = maps(trail['id'])
        image_data = photos(trail['id'])
        trip = trips(trail['id'])

        if map_data == [] and image_data == [] and trip == []:
            map_url = None
            image = None
            length = None
            duration = None
            intensity = None

        elif map_data != [] and image_data != [] and trip != []:
            map_link = map_data.pop()
            map_url = map_link['url']

            length = trip['length_miles']
            duration = trip['duration']
            intensity = trip["intensity"]

            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']

            except:
                pass

        elif map_data != [] and image_data != [] and trip == []:

            map_link = map_data.pop()
            map_url = map_link['url']

            length = None
            duration = None
            intensity = None

            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']

            except:
                pass

        elif map_data != [] and image_data == [] and trip != []:

            map_link = map_data.pop()
            map_url = map_link['url']

            length = trip['length_miles']
            duration = trip['duration']
            intensity = trip["intensity"]

            image = None

        elif map_data == [] and image_data != [] and trip != []:

            map_url = None

            length = trip['length_miles']
            duration = trip['duration']
            intensity = trip["intensity"]

            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']

            except:
                pass

        elif map_data != [] and image_data == [] and trip == []:
 
            map_link = map_data.pop()
            map_url = map_link['url']

            image = None

            length = None
            duration = None
            intensity = None

        elif map_data == [] and image_data == [] and trip != []:

            length = trip['length_miles']
            duration = trip['duration']
            intensity = trip["intensity"]

            map_url = None

            image = None

        elif map_data == [] and image_data != [] and trip == []:

            map_url = None

            length = None
            duration = None
            intensity = None

            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']

            except:
                pass

        print trail_id, trail_name, map_url, image, length, duration, intensity

        trail = Trail.query.get(trail_id)

        if trail is not None:

            new_trail = Trail(trail_id=trail_id,
                              trail_name=trail_name,
                              maps=map_url,
                              image=image,
                              length=length,
                              duration=duration,
                              intensity=intensity)

            db.session.add(new_trail)

    db.session.commit()


# def add_images():

#     trails = trailheads()

#     for trail in trails:

#         image_data = photos(trail['id'])

#         if image_data != []:
#             image_url = image_data.pop()
#             image = image_url['flickr_url']

#         else:
#             image = None

#             new_trail = trails.insert(image=image)
#             new_trail.execute()


# def add_searches():

#     trails = trailheads()

#     for trail in trails:

#         trip = trips(trail['id'])

#         if trip:
#             length = trip['length_miles']
#             duration = trip['duration']
#             intensity = trip["intensity"]

#         else:
#             length = None
#             duration = None
#             intensity = None

#             new_trail = trails.insert()
#             new_trail.execute(length=length, duration=duration, intensity=intensity)


# def seed_park_table():
#     """Data for park table"""

#     parks = trailheads()

#     for park in parks:
#         trail_id = park['id']
#         latitude = park['latitude']
#         longitude = park['longitude']

#         description = park['description']
#         park_name = park['park_name']

#     for park in parks:

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
    seed_trail_table()
