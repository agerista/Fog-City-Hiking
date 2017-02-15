import requests
import os
from model import db, connect_to_db, Park
from server import app

SECRET = os.environ["YELP_SECRET"]
Y_ID = os.environ["YELP_ID"]
API_ROOT = "https://api.yelp.com/v3/"

def obtain_bearer_token():
    """Request authorization tokens"""

    endpoint = "https://api.yelp.com/oauth2/token"


    response = requests.post(endpoint, data={"client_secret": SECRET,
                                             "client_id": Y_ID,
                                             "grant_type": "client_credentials"})

    bearer_token = response.json()['access_token']

    return bearer_token

def get_header():
    """get header and token information"""

    token = obtain_bearer_token()
    headers = {"Authorization": 'Bearer {}'.format(token)}

    return headers


def get_business_ids():
    """Get the business id for each park"""

    all_id = []

    endpoint = "businesses/search"

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



        response = requests.get(endpoint, params=data, headers=get_header())

        business = response.json()

        business_id = business['businesses'][0]['id']

        all_id.append(business_id)

    print all_id
        # db.session.query(Park).filter(Park.park_name == name).update({"yelp_id": id})  # set the second yelp_id in a variable

        #match response to trail id
        #add business id to park table
    return all_id


def yelp_information(business_id):
    """Returns image, rating, and open hours when given a park_id"""

    endpoint = API_ROOT + "businesses/{}".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    info = response.json()

    yelp_info = {}

    image_url = info['image_url']
    rating = info['rating']
    print image_url, rating

    ### key error if hours are not included.

    # opens = info['hours']    # [:]["start"]
    # closes = info['hours']   # [:]["end"]

    yelp_info["image_url"] = image_url,
    yelp_info["rating"] = rating
    # ["opens"] = opens,
    # ["closes"] = closes
    print yelp_info
    return yelp_info


def get_yelp_reviews(business_id):
    """Given a business_id returns yelp reviews"""

    endpoint = API_ROOT + "businesses/{}/reviews".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    information = response.json()
    print information

    # yelp_reviews = {"review_url": [],
    #                 "review_text": [],
    #                 "rating": []}

        # url = info[0]
        # text = info[1]
        # rating = info[2]


        # yelp_reviews["review_url"].append(url)
        # yelp_reviews["review_text"].append(text)
        # yelp_reviews["rating"].append(rating)

        # print url, text, rating
    # return yelp_reviews


if __name__ == "__main__":

    connect_to_db(app)
    obtain_bearer_token()
    # get_business_ids()
    # yelp_information('miller-knox-regional-park-richmond')
    get_yelp_reviews('miller-knox-regional-park-richmond')
