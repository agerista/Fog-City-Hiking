
import requests
import os
from model import db, connect_to_db, Park
import forecastio

api_key = os.environ["DARK_KEY"]


def weather_forecast():
    """Get the weather"""

    # Cap is 1,000 calls per day
    # db.session.query(Park.latitude, Park.longitude).filter_by(city.distinct().all()
    coordinates = [("San Francisco", 37.7749, -122.4194), ("Oakland", 37.8044, -122.2711), ("Berkeley", 37.8716, -122.2727), ("Marin", 38.0834, -122.7633), ("Pacifica", 37.6138, -122.4869)]

    weather_info = {}

    for coordinate in coordinates:

        city = {}

        lat = coordinate[1]
        city["latitude"] = lat

        lng = coordinate[2]
        city["longitude"] = lng

        weather = forecastio.load_forecast(api_key, lat, lng)

        hour = weather.hourly()
        summary = hour.summary
        city["summary"] = summary

        icon = hour.icon
        city["icon"] = icon

        weather_info["city"] = city
        print weather_info

    return weather_info


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    weather_forecast()
