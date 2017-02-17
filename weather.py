import requests
import os
# from model import db, connect_to_db, Park
# from server import app
import forecastio

api_key = os.environ["DARK_KEY"]


def weather_forecast():
    """Get the weather



    """

    # Cap is 1,000 calls per day
    # db.session.query(Park.latitude, Park.longitude).filter_by(city).distinct().all()
    coordinates = [(37.7749, -122.4194), (37.8044, -122.2711), (37.8716, -122.2727), (38.0834, -122.7633), (37.6138, -122.4869)]
    info = []
    weather_info = []

    for coordinate in coordinates:

        lat = coordinate[0]
        info.append(lat)
        lng = coordinate[1]
        info.append(lng)

        weather = forecastio.load_forecast(api_key, lat, lng)

        hour = weather.hourly()
        summary = hour.summary
        info.append(summary)

        icon = hour.icon
        info.append(icon)

        weather_info.append(info)
        print weather_info

    return weather_info


if __name__ == "__main__":
    # connect_to_db(app)
    weather_forecast()
