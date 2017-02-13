import requests
import os
from model import db, connect_to_db, Park
from server import app
import forecastio

api_key = os.environ["DARK_KEY"]


# def weather_forecast():
#     """Get the weather"""


    # Cap is 1,000 calls per day 
    # coordinates = db.session.query(Park.latitude, Park.longitude).distinct().first()

    # for coordinate in coordinates:

    #     type(coordinate)
    #     print coordinate

    #     lat = coordinate[0]
    #     lng = coordinate[1]

weather = forecastio.load_forecast(api_key,50.0,10.0)
        # weather = forecastio.load_forecast(api_key, lat, lng)
        # weather = forecastio.load_forecast(api_key, coordinate[0], coordinate[1])

    # return weather


if __name__ == "__main__":
    connect_to_db(app)
    weather_forecast()
