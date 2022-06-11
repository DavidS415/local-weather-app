from flask import Flask, current_app
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from datetime import date
import requests
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

class WeatherApi(Resource):
    def get(self, ip_address):

        location = requests.get("https://geolocation-db.com/json/" + ip_address)
        data = location.text
        formated_data = json.loads(data)
        l = formated_data['latitude']
        latitude = str(l)
        lo = formated_data['longitude']
        longitutde = str(lo)

        weather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitutde+"&appid=e63815661b8d8566fb54c8fdc5a0e85e&units=imperial")
        weather_data = weather.text
        formated_weather_data = json.loads(weather_data)

        now = date.today()
        current = now.strftime('%Y-%m-%d')
        events = requests.get("https://app.ticketmaster.com/discovery/v2/events?apikey=9mLUBOt5QXfFkITv6RWYbMNupl7qAp4Z&latlong="+latitude+","+longitutde+"&radius=50&unit=miles&locale=*&startDateTime="+current+"T00:00:00Z&endDateTime="+current+"T23:59:00Z")
        events_data = events.text
        formated_events_data = json.loads(events_data)

        return {
            'events': formated_events_data,
            'weather': formated_weather_data
        }

api.add_resource(WeatherApi, '/<string:ip_address>')

if __name__ == '__main__':
    app.run(debug=True)