import requests
import os

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

    data = {"term": "golden-gate-park",
            "categories": "parks",
            "latitude": 37.767413217936834,
            "longitude": -122.42820739746094,
            "limit": 3}

    response = requests.get(endpoint, params=data, headers=headers)

    return response.json()

if __name__ == "__main__":

    get_business_id()
