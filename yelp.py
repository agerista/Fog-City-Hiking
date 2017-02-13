import requests
import os

SECRET = os.environ["YELP_SECRET"]
Y_ID = os.environ["YELP_ID"]

response_access = requests.post("https://api.yelp.com/oauth2/token", SECRET, Y_ID)

def get_business_id():
    """Get the business id for each park"""

    endpoint = "https://api.yelp.com/v3/businesses/search"

    data = {"term": "Golden Gate Park",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "limit": 1}

    response = requests.get(endpoint, data=data)

    return response.json()
