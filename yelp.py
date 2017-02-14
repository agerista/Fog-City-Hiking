import requests
import os
from model import db, connect_to_db, Park
from server import app

SECRET = os.environ["YELP_SECRET"]
Y_ID = os.environ["YELP_ID"]
API_ROOT = "https://api.yelp.com/oauth2/token"


def obtain_bearer_token():
    """Request authorization tokens"""

    endpoint = API_ROOT

    response = requests.post(endpoint, data={"client_secret": SECRET,
                                             "client_id": Y_ID,
                                             "grant_type": "client_credentials"})

    bearer_token = response.json()['access_token']

    return bearer_token


def get_business_id():
    """Get the business id for each park"""

    endpoint = "https://api.yelp.com/v3/businesses/search"

    token = obtain_bearer_token()
    headers = {"Authorization": 'Bearer {}'.format(token)}

    searches = db.session.query(Park.park_name, Park.latitude, Park.longitude).limit(5).all()

    for search in searches:
        name = search[0]
        lat = search[1]
        lng = search[2]

        data = {"term": name,
                "categories": "parks",
                "latitude": lat,
                "longitude": lng,
                "limit": 3}

        response = requests.get(endpoint, params=data, headers=headers)

        # db.session.query(Park).filter(Park.park_name == name).update({"yelp_id": id})  # set the second yelp_id in a variable

        #match response to trail id
        #add business id to park table
        return response



    

if __name__ == "__main__":

    connect_to_db(app)
    get_business_id()
