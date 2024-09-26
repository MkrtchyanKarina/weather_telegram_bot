import requests
from tokens import photo_token, weather_token


def wind_direction(deg):
    if 0 <= deg <= 23 or 337 <= deg <= 360:
        return "N"
    elif 24 <= deg <= 68:
        return "NE"
    elif 69 <= deg <= 113:
        return "E"
    elif 114 <= deg <= 158:
        return "SE"
    elif 159 <= deg <= 203:
        return "S"
    elif 204 <= deg <= 248:
        return "SW"
    elif 249 <= deg <= 293:
        return "W"
    else:
        return "NW"


def get_photo(query):
    url = "https://api.unsplash.com//photos/random"
    params = {'client_id': photo_token, 'query': query}
    response = requests.get(url=url, params=params)
    if response.ok:
        return response.json()['urls']['small']
    else:
        return ''


def weather_json_parse(response):
    if response.ok:
        information = response.json()
        description = information['weather'][0]['description']  # rain, snow and ect.

        temperature = int(information['main']['temp'])
        if temperature > 0:
            temperature = "+" + str(temperature)
        else:
            temperature = str(temperature)

        temp_feels_like = int(information['main']['feels_like'])
        if temp_feels_like > 0:
            temp_feels_like = "+" + str(temp_feels_like)
        else:
            temp_feels_like = str(temp_feels_like)

        pressure = str(int(int(information['main']['pressure']) * 0.7506))
        humidity = information['main']['humidity']
        wind_speed = str(int(information['wind']['speed']))
        wind_dir = wind_direction(int(information['wind']['deg']))

        result = (
            f"Now in {information['name']} {temperature}, {description}.\nIt feels like "
            f"{temp_feels_like}.\nAtmospheric pressure is {pressure} mmHg.\n"
            f"Humidity is {humidity}%.\nWind: {wind_speed} m/s ({wind_dir})")

        return get_photo(description), result

    else:
        if response.status_code == 404:
            return '', ''
        else:
            return -1


def current_weather(city):
    params = {'q': city, 'appid': weather_token, 'units': 'metric'}
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url=url, params=params)
    return weather_json_parse(response)


