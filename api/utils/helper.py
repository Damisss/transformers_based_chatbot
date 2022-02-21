from math import floor
import os 
from flask import jsonify, request
import json
import requests

def get_city():
    APIKEY = os.environ['GEATCITYAPIKEY']
    print('APIKEYY', APIKEY)
    url = f'https://api.freegeoip.app/json/?apikey={APIKEY}'
    res = requests.get(url)
    data = json.loads(res.text)
    city = data['city']
    return city


def get_weather(*, city:str):
    APIKEY = os.environ['GEATWEATHERAPIKEY']
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={APIKEY}&units=metric')
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        humidity = main['humidity']
        wind = data['wind']
        speed = round(wind['speed'] * 3.6) if wind['speed'] else ''
        return jsonify({
            "message": [{'temperature': f"{round(main['temp'])}\u00B0C", 'humidity': f'{humidity}%', 'wind': f'{speed} Km/hr'}],
            "status_code": 200,
            "intent":"GetWeather",
            "type": "bot",
        })
       
    return jsonify({
        "message": "Sorry!! we are unable to process your request at this time. Please try again later.",
        "status_code": 500,
    })