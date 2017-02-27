"""Dark Sky API call to get Bay Area forecasts. Cap is 1,000 calls per day"""

import requests
import os
from model import db, connect_to_db, Park
import forecastio

api_key = os.environ["DARK_KEY"]


def weather_forecast():
    """Get the weather

    Structure:

    weather_info["city": {"latitude": 37.7749,
                          "longitude": -122.4149,
                          "icon": "sun",
                          "summary": "Sunny throughout the day"]

    Example output:

    [{'latitude': 37.7749, 'icon': u'rain', 'longitude': -122.4194,\
    'summary': u'Breezy tonight and light rain starting tonight,\
    continuing until tomorrow evening.'}
    """

    coordinates = db.session.query(Park.latitude, Park.longitude, Park.city).filter(
        Park.city != None).distinct(Park.city).all()
    # coordinates = [("San Francisco", 37.7749, -122.4194), ("Oakland", 37.8044, -122.2711),
                   # ("Berkeley", 37.8716, -122.2727), ("Marin", 38.0834, -122.7633),
                   # ("Pacifica", 37.6138, -122.4869)]

    print coordinates
    weather_info = []

    for coordinate in coordinates:

        city = {}

        city["city"] = coordinate[2]

        city["latitude"] = coordinate[0]

        city["longitude"] = coordinate[1]

        weather = forecastio.load_forecast(api_key, city["latitude"], city["longitude"])

        day = weather.daily()
        summary = day.summary
        city["summary"] = summary


        # temperature = day.temperature
        # city["temperature"] = temperature

        icon = day.icon
        city["icon"] = icon

        weather_info.append(city)
    print weather_info

    return weather_info


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    weather_forecast()
