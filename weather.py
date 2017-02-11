import requests
import os
import forecastio
from model import db, connect_to_db, Park
from server import app

def weather_forecast():
    api_key = os.environ['DARK_KEY']
    # lat = 37.7749
    # lng = -122.4194

    coordinates = db.session.query(Park.latitude, Park.longitude).first()
    # seperate query call for lat and long needed

    for coordinate in coordinates:
        forecastio.load_forecast(api_key, lat, lng)

        byHour = forecast.hourly()
        weather = byHour.summary

    return weather

if __name__ == "__main__":
    connect_to_db(app)
