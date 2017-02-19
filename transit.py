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


def trips():
    """Get trips"""

    key = os.environ['TRANSIT_KEY']
    endpoint = API_ROOT + "/trips"
    data = {"key": key}

    response = requests.get(endpoint, data=data)
    print response

    return response


def add_attributes():
    """Add attributes to trail"""

    trails = trailheads()

    for trail in trails[100:150]:
        trail_id = trail['id']

        attribute_data = attributes(trail_id)
        print attribute_data

        attribute_list = attribute_data
        if attribute_list != []:

            i = 0

            while i < len(attribute_list):

                if attribute_list[i]["name"] == 'Drinking Water':
                    water = True
                    print "water"

                if attribute_list[i]["name"] == "Restrooms":
                    restrooms = True
                    print "restrooms"

                if attribute_list[i]["name"] == "Visitor Center":
                    visitor_center = True
                    print "visit"

                if attribute_list[i]["name"] == "Parking":
                    parking = True
                    print "parking"

                if attribute_list[i]["name"] == "Birding":
                    birding = True
                    print "birding"

                if attribute_list[i]["name"] == "Picnic Tables":
                    picnic_tables = True
                    print "Picnic"

                if attribute_list[i]["name"] == "Dirt":
                    dirt_path = True
                    print "dirt"

                if attribute_list[i]["name"] == "Paved":
                    paved_path = True
                    print "paved"

                if attribute_list[i]["name"] == "Gravel":
                    gravel_path = True
                    print "gravel"

                if attribute_list[i]["name"] == "No Dogs Allowed":
                    dog_free = True
                    print "dog_free"

                if attribute_list[i]["name"] == "Dogs Allowed On-leash":
                    dogs_on_leash = True
                    print "dogs leash"

                if attribute_list[i]["name"] == "Dogs Allowed Off-leash":
                    dogs_off_leash = True
                    print "Off-leash"

                if attribute_list[i]["name"] == "Transit":
                    transit_near = True
                    print "transit"

                i += 1

    return "done"


trailheads()
attributes(trail_id)
photos(trail_id)
maps(trail_id)
trips()
