import requests
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h2>Laboratorio 9</h2>'


@app.route('/<place>')
def get_lat_lon(place):
    url = f'https://nominatim.openstreetmap.org/search?q={place}&format=json'
    r_coordinates = requests.get(url)
    jsonData = r_coordinates.json()
    if len(jsonData) == 0:
        return ""
    lat_res = jsonData[0]['lat']
    lon_res = jsonData[0]['lon']
    print("Latitud:", lat_res)
    print("Longitud:", lon_res)

    url_weather_daily = f'https://api.open-meteo.com/v1/forecast?latitude={lat_res}&longitude={lon_res}&forecast_days' \
                        f'=2&daily=temperature_2m_max,temperature_2m_min&timezone=GMT'
    # url_weather_hourly = f'https://api.open-meteo.com/v1/forecast?latitude={lat_res}&longitude={
    # lon_res}&forecast_days=2&hourly=temperature_2m'

    r_weather = requests.get(url_weather_daily)
    weather_json = r_weather.json()

    response = {}

    temperature = {'max': weather_json['daily']['temperature_2m_max'][0],
                   'min': weather_json['daily']['temperature_2m_min'][0]}

    response['temperature'] = temperature

    minLat = jsonData[0]['boundingbox'][0]
    maxLat = jsonData[0]['boundingbox'][1]
    minLon = jsonData[0]['boundingbox'][2]
    maxLon = jsonData[0]['boundingbox'][3]

    url_places = f'https://api.openstreetmap.org/api/0.6/map.json?bbox={minLon},{minLat},{maxLon},{maxLat}'
    r_places = requests.get(url_places)
    places_json = r_places.json()

    restaurants = []

    for element in places_json['elements']:
        if len(restaurants) == 3:
            break
        if 'tags' in element:
            if 'amenity' in element['tags']:
                if element['tags']['amenity'] == 'restaurant':
                    result = {}
                    if 'name' in element['tags']:
                        result['name'] = element['tags']['name']
                    if 'addr:street' in element['tags']:
                        result['street'] = element['tags']['addr:street']
                    if 'addr:housenumber' in element['tags']:
                        result['house_number'] = element['tags']['addr:housenumber']
                    if 'amenity' in element['tags']:
                        result['amenity'] = element['tags']['amenity']
                    restaurants.append(result)

    response['restaurants'] = restaurants

    return response


if __name__ == "__main__":
    app.run(debug=False, port=5000)
