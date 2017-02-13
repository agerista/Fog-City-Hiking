from sqlalchemy import *
from model import *
from server import app
from transit import *


                  
                  # image=image,
                  # length=length,
                  # duration=duration,
                  # intensity=intensity)

def seed_trail_table():
    """Information for trail table"""

    trails = trailheads()

    for trail in trails:
        trail_id = trail['id']
        trail_name = trail['name']

        print trail_id, trail_name

#         # map_data = maps(trail['id'])
#         # image_data = photos(trail['id'])
#         # trip = trips(trail['id'])

#         # if map_data == [] and image_data == [] and trip == []:
#         #     map_url = None
#         #     image = None
#         #     length = None
#         #     duration = None
#         #     intensity = None

#         # elif map_data != [] and image_data != [] and trip != []:
#         #     map_link = map_data.pop()
#         #     map_url = map_link['url']

#         #     length = trip['length_miles']
#         #     duration = trip['duration']
#         #     intensity = trip["intensity"]

#         #     image_url = image_data.pop()

#         #     try:
#         #         image = image_url['flicker_url']

#         #     except:
#         #         pass
        

        trail = Trail.query.get(trail_id)


        new_trail = Trail(trail_id=trail_id,
                          trail_name=trail_name)

        if trail is None:
            db.session.add(new_trail)

    db.session.commit()
    print "done committing trails"

# def add_maps():

#     trails = trailheads()

#     for trail in trails[40:50]:

#         trail_id = trail['id']
#         map_data = maps(trail['id'])

#         if map_data != []:
#             map_link = map_data.pop()
#             map_url = map_link['url']

#         else:
#             map_url = None
#         print map_url

#         print trail_id, map_url

#         trail = Trail.query.filter_by(trail_id=trail_id).first()
#         # trail.maps == map_url

#         setattr(trail, 'maps', map_url)

#         db.session.commit()

#         # if trail is not None:

#         #     db.session.query().filter(Trail.trail_id == trail_id).update(maps, map_url)

    

#     print "done with maps"
#             # m = new_trail.insert()
#             # m.execute(maps=map_url)

            



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
    # add_maps()
