from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h2>Laboratorio 9</h2>'

@app.route('/<place>')
def get_lat_lon(place):
    url = f'https://nominatim.openstreetmap.org/search?q={place}&format=json'
    r_coordinates = requests.get(url)
    jsonData = r_coordinates.json()
    lat_res = jsonData[0]['lat']
    lon_res = jsonData[0]['lon']
    print("Latitud:", lat_res)
    print("Longitud:", lon_res)

    url_weather_daily = f'https://api.open-meteo.com/v1/forecast?latitude={lat_res}&longitude={lon_res}&forecast_days=2&daily=temperature_2m_max,temperature_2m_min&timezone=GMT'
    # url_weather_hourly = f'https://api.open-meteo.com/v1/forecast?latitude={lat_res}&longitude={lon_res}&forecast_days=2&hourly=temperature_2m'

    r_weather = requests.get(url_weather_daily)
    weather_json = r_weather.json()

    next_day_temperature_max = weather_json['daily']['temperature_2m_max'][1]
    print(f"La temperatura máxima será {next_day_temperature_max}°C")
    next_day_temperature_min = weather_json['daily']['temperature_2m_min'][1]
    print(f"La temperatura minima será {next_day_temperature_min}°C")

    return weather_json['daily']



if __name__ == "__main__":
    app.run(debug=True, port=5000)