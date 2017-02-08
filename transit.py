import requests
import os


def trailheads():
    """Request all trailheads within x miles of a given latitue and longitude"""

    key = os.environ['TRANSIT_KEY']
    endpoint = "https://api.transitandtrails.org/api/v1/trailheads"
    data = {"key": key,
            "distance": 25,
            "latitude": 37.7749,
            "longitude": -122.4194}

    response = requests.get(endpoint, data=data)

    return response


def attributes(trail_id):
    """Request amenities for a designated trailhead"""

    key = os.environ['TRANSIT_KEY']
    endpoint = "https://api.transitandtrails.org/api/v1/trailheads/{}/attributes".format(trail_id)
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response


def photos(trail_id):
    """Request photos for a designated trailhead"""

    key = os.environ['TRANSIT_KEY']
    endpoint = "https://api.transitandtrails.org/api/v1/trailheads/{}/photos".format(trail_id)
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response

def maps(trail_id):
    """Get maps for your trail"""

    key = os.environ['TRANSIT_KEY']
    endpoint = "https://api.transitandtrails.org/api/v1/trailheads/{}/maps".format(trail_id)
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response


def trips(trail_id):
    """Get trips"""

    key = os.environ['TRANSIT_KEY']
    endpoint = "https://api.transitandtrails.org/api/v1/trailheads"
    data = {"key": key}

    response = requests.get(endpoint, data=data)

    return response



"""

    In [12]: for park in tjson[:25]:
    ...:     print "{} {}".format(park['id'], park['name']
    ...:     
    ...:     
    ...:     )
    ...:     
1 Dornan Drive Parking Lot (South)
2 Seacliff Drive Walk-In Entrance
3 Dornan Drive Parking Lot (Picnic Area 2)
4 Dornan Drive Parking Lot (Picnic Area 1)
5 Canal Blvd Walk-In Entrance
6 Crest Avenue Walk-In Entrance
37 Estancia Court Walk-In Entrance
38 Marksmanship Range Staging Area
39 Marciel Road Day Use Parking
40 Knowland Park
41 Marciel Road Park Entrance/Kiosk
42 Redwood Road Walk-In Entrance - Soaring Hawk Trail (south)
43 Clyde Woolridge Staging Area
44 Paddock Drive Walk-In Entrance
45 Chabot Park Walk-In Entrance
46 Neptune Drive Park Entrance-Oyster Bay Regional Shoreline
47 Marciel Gate Staging Area
48 West Winton Avenue Park Entrance
49 Heyer Avenue Walk-In Entrance
50 Main Entrance Staging Area
51 Winifred Drive Walk-In Entrance
52 Columiba Drive Walk-In Entrance
53 Woodroe Avenue Park Entrance
54 Main Parking Area
55 Grant Avenue Walk-In Entrance

In [13]: attributes(41).json()
Out[13]: 
[{u'category': 2,
  u'category_name': u'Amenities',
  u'id': 3,
  u'name': u'Visitor Center'},
 {u'category': 2,
  u'category_name': u'Amenities',
  u'id': 2,
  u'name': u'Restrooms'}]

In [14]: attributes(54).json()
Out[14]: 
[{u'category': 2,
  u'category_name': u'Amenities',
  u'id': 2,
  u'name': u'Restrooms'}]

In [15]: attributes(46).json()
Out[15]: 
[{u'category': 5,
  u'category_name': u'Barrier Free (limited mobility)',
  u'id': 31,
  u'name': u'Accessible Trail'},
 {u'category': 5,
  u'category_name': u'Barrier Free (limited mobility)',
  u'id': 6,
  u'name': u'Accessible Restrooms'},
 {u'category': 4, u'category_name': u'Surface', u'id': 30, u'name': u'Paved'},
 {u'category': 4, u'category_name': u'Surface', u'id': 28, u'name': u'Dirt'},
 {u'category': 3,
  u'category_name': u'Activities',
  u'id': 17,
  u'name': u'Birding'},
 {u'category': 10,
  u'category_name': u'Regional Trail',
  u'id': 33,
  u'name': u'San Francisco Bay Trail'},
 {u'category': 5,
  u'category_name': u'Barrier Free (limited mobility)',
  u'id': 27,
  u'name': u'Accessible Picnic Area'},
 {u'category': 2,
  u'category_name': u'Amenities',
  u'id': 18,
  u'name': u'Primary Park Entrance'},
 {u'category': 2,
  u'category_name': u'Amenities',
  u'id': 2,
  u'name': u'Restrooms'},
 {u'category': 2,
  u'category_name': u'Amenities',
  u'id': 4,
  u'name': u'Parking'},
 {u'category': 2,
  u'category_name': u'Amenities',
  u'id': 22,
  u'name': u'Picnic Tables'},
 {u'category': 3,
  u'category_name': u'Activities',
  u'id': 11,
  u'name': u'Hiking'}]
"""
