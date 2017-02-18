import requests
import os
from model import db, connect_to_db, Park

# Call limit to yelp api is 25,000/day

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


def yelp_information(business_id):
    """Returns image, rating, and open hours when given a park_id"""

    endpoint = API_ROOT + "businesses/{}".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    info = response.json()
    print info

    yelp_info = {}

    image_url = info['image_url']
    rating = info['rating']
    print image_url, rating

    ### key error if hours are not included.

    ## opens = info['hours']    # [:]["start"]
    ## closes = info['hours']   # [:]["end"]

    yelp_info["image_url"] = image_url,
    yelp_info["rating"] = rating
    ## ["opens"] = opens,
    ## ["closes"] = closes
    print yelp_info
    return yelp_info


def get_yelp_reviews(business_id):
    """Given a business_id returns yelp reviews

       reviews{user: [],
               text: [],
               rating: [],
               url: []}

    """

    endpoint = API_ROOT + "businesses/{}/reviews".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    information = response.json()

    review_list = information['reviews']

    i = 0
    yelp_reviews = {}
    reviews = {}

    while i < len(review_list):

        name = review_list[i]['user']['name']
        reviews['name'] = name

        text = review_list[i]['text']
        reviews['text'] = text

        rating = review_list[i]['rating']
        reviews['rating'] = rating

        url = review_list[i]['url']
        reviews['url'] = url

        yelp_reviews["review"] = reviews

        i += 1
        print yelp_reviews



    return yelp_reviews


def get_business_ids():
    """Get the business id for each park"""

    endpoint = API_ROOT + "businesses/search"

    searches = db.session.query(Park.park_name, Park.latitude, Park.longitude).all()

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

        try:
            business_id = business['businesses'][0]['id']

            print business_id
            db.session.query(Park).filter(Park.park_name == name).update({"yelp_id": business_id})

            db.session.commit()
        except IndexError:
            pass

    print "done committing yelp ids"


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    obtain_bearer_token()
    # get_business_ids()
    yelp_information(business_id)
    get_yelp_reviews(business_id)
