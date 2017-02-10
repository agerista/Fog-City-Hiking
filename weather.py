import requests
import os
import forecastio

api_key = os.environ['DARK_KEY']
lat = 37.7749
lng = -122.4194

forecast = forecastio.load_forecast(api_key, lat, lng)

byHour = forecast.hourly()
print byHour.summary
print byHour.icon
