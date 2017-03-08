# H1 Welcome to Fog City Hiking!

About a year ago, I bought a car, which opened a world of hiking opportunities outside of the city. With all of these opportunities, came the problem of looking up weather, trails, and yelp reviews separately to figure out where to go hiking that day. This project was the perfect opportunity to solve that problem.

# H1 Tech Stack

Fog City Hiking uses the following technologies:

* PostgreSQL
* SQLAlchemy
* Flask
* Python
* JavaScript
* AJAX
* JQuery
* Jinja
* Bootstrap

API's Used:

* Dark Sky
* Google Maps
* Transit and Trails
* Yelp


The first step was to use Python to do a call to the Transit and Trails API to gather all of the data about trails in the Bay Area so that I could build a SQL database. On the homepage, you can see a map of the Bay Area thanks to the Google Maps API.  A map alone is not very interesting, so I queried the database to find all of cities that have trails. With that information, I called the Dark Sky API to get weather information, which I rendered with AJAX to put climacons and a weather summary onto the map.

The parks and trails are all listed alphabetically, and if you click through any of the entries, you can see the results of a call to the Yelp API, which displays photos and reviews of a particular place, along with a brief description and attributes of the trail from a sqlalchemy query.

If you don’t know the name of the park or trail you can use the search page. You can input a city or a trail length and a sqlalchemy query will return up to 5 trails. At the same time a call to the Yelp API and the magic of JSON and Jinja will return photos and reviews. The checkboxes next to the results allow you to save a hike. If you’ve already done the hike, you can add some details of your experience. If not, you can bookmark the hike for later use. Those hikes will show up on your profile page when you are logged into a Flask session.  For security, all passwords have been passed through a hashing algorithm. 
