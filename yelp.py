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

        review = [user, review, rating, url]  

    """

    endpoint = API_ROOT + "businesses/{}/reviews".format(business_id)

    response = requests.get(endpoint, headers=get_header())

    information = response.json()
    print information

    reviews = []

    i = 0
    base = information['reviews']

    while i < len(base):

        user = base[i]['user']['name']
        reviews.append(user)
        print user
        print "-----"

        review = base[i]['text']
        reviews.append(review)
        print review
        print "-----"

        rating = base[i]['rating']
        reviews.append(rating)
        print rating
        print "-----"

        url = base[i]['url']
        reviews.append(url)
        print url
        print "-----"

        i += 1

    print reviews
    return reviews


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    obtain_bearer_token()
    # get_business_ids()
    # yelp_information('miller-knox-regional-park-richmond')
    # get_yelp_reviews('miller-knox-regional-park-richmond')
