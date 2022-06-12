from types import CoroutineType
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
        weather_data = weather.json()
        current_temp = weather_data['main']['temp']
        current_weather = weather_data['weather'][0]['main']
        current_high = weather_data['main']['temp_max']
        current_low = weather_data['main']['temp_min']

        now = date.today()
        current = now.strftime('%Y-%m-%d')
        print(current)
        events = requests.get("https://app.ticketmaster.com/discovery/v2/events?apikey=9mLUBOt5QXfFkITv6RWYbMNupl7qAp4Z&latlong="+latitude+","+longitutde+"&radius=200&unit=miles&locale=*&startDateTime="+current+"T00:00:00Z&endDateTime="+current+"T23:59:00Z")
        events_data = events.json()
        data = events_data['_embedded']['events']
        number_events = events_data['page']['totalElements']
        if number_events < 1:
            events = 'No events'
        else:
            names = []
            url = []
            venue = []
            locations = []
            events = number_events
            for i in data:
                names.append(i['name'])
                url.append(i['url'])
                venue.append(i['_embedded']['venues'][0]['name'])
                city = (i['_embedded']['venues'][0]['city']['name']) + ', ' + (i['_embedded']['venues'][0]['state']['stateCode'])
                locations.append(city)

        return {
            'events': {
                'events': events,
                'names': names,
                'url': url,
                'venue': venue,
                'locations': locations
            },
            'weather': {
                'current_temp': current_temp,
                'current_weather': current_weather,
                'current_high': current_high,
                'current_low': current_low
            }
        }

api.add_resource(WeatherApi, '/<string:ip_address>')

if __name__ == '__main__':
    app.run(debug=True)