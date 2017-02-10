from sqlalchemy import func
from model import User
from model import Hike
from model import Trail
from model import Park
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

        if map_data == []:
            map_url = None
        else:
            map_link = map_data.pop()
            map_url = map_link['url']

        image_data = photos(trail['id'])

        if image_data == []:
            image = None

        elif image_data is not None:
            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']

            except:
                pass

        trip = trips(trail['id'])

        if trip:
            length = trip['length_miles']
            duration = trip['duration']
            intensity = trip["intensity"]

        else:
            length = None
            duration = None
            intensity = None

        print trail_id, trail_name, map_url, image, length, duration, intensity
        print
        print

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


def seed_park_table():
    """Data for park table"""

    parks = trailheads()

    for park in parks:
        trail_id = park['trail_id']
        latitude = park['latitude']
        longitude = park['longitude']

        description = park['description']
        park_name = park['park_name']

        print park_name, trail_id

        image_data = photos(trail['id'])

        if image_data == []:
            image = None

        elif image_data is not None:
            image_url = image_data.pop()

            try:
                image = image_url['flicker_url']

            except:
                pass

        park = Park(latitude=latitude,
                    longitude=longitude,
                    description=description,
                    park_name=park_name,
                    image=image)

        db.session.add(park)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # seed_park_table()
    seed_trail_table()
