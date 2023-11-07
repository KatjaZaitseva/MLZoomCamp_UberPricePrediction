import requests

#the app.route that we use in POST method
url = "http://localhost:9696/predict"


ride_info = {
    "job": 3.1, 
    "surge_multiplier": 1.1, 
    "latitude": 42.3429,
    "longitude": -71.1003,
    "temperature": 34.5,
    "apparenttemperature": 30.8,
    "precipintensity": 0.01,
    "precipprobability": 0.01,
    "humidity": 0.84,
    "windspeed": 8.66,
    "windgust": 9.17,
    "visibility": 8,
    "source": "Back Bay",
    "name": "UberX",
    "hour": 11,
    "day": 28
    }

response = requests.post(url, json=ride_info).json()

print(response)