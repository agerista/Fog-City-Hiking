import requests
import os
import forecastio
from model import db, connect_to_db, Park
from server import app


api_key = os.environ["DARK_KEY"]


def weather_forecast():

    coordinates = db.session.query(Park.latitude, Park.longitude).distinct().all()

    for coordinate in coordinates:

        lat = coordinate[0]
        lng = coordinate[1]

        weather = forecastio.load_forecast(api_key, lat, lng)
  


    return weather


if __name__ == "__main__":
    connect_to_db(app)
    weather_forecast()
