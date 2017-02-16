import requests
import os

API_ROOT = "https://api.transitandtrails.org/api/v1"


def trailheads():
    """Request all trailheads within x miles of a given latitue and longitude"""

    key = os.environ['TRANSIT_KEY']
    endpoint = API_ROOT + "/trailheads"
    data = {"key": key,
            "distance": 50,
            "latitude": 37.7749,
            "longitude": -122.4194}

    response = requests.get(endpoint, data=data)

    return response.json()


def attributes(trail_id):
    """Request amenities for a designated trailhead"""

    key = os.environ['TRANSIT_KEY']
    endpoint = API_ROOT + "/trailheads/{}/attributes".format(trail_id)
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response.json()


def photos(trail_id):
    """Request photos for a designated trailhead"""

    key = os.environ['TRANSIT_KEY']
    endpoint = API_ROOT + "/trailheads/{}/photos".format(trail_id)
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response.json()


def maps(trail_id):
    """Get maps for your trail"""

    key = os.environ['TRANSIT_KEY']
    endpoint = API_ROOT + "/trailheads/{}/maps".format(trail_id)
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response.json()


def trips(trail_id):
    """Get trips"""

    key = os.environ['TRANSIT_KEY']
    endpoint = API_ROOT + "/trips"
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response.json()




# for park in tjson[:25]:
#     ...:     print "{} {}".format(park['id'], park['name']