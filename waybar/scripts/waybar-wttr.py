#!/usr/bin/env python

import json
import requests
from datetime import datetime

WEATHER_CODES = {
    '113': '☀️ ',
    '116': '⛅ ',
    '119': '☁️ ',
    '122': '☁️ ',
    '143': '☁️ ',
    '176': '🌧️',
    '179': '🌧️',
    '182': '🌧️',
    '185': '🌧️',
    '200': '⛈️ ',
    '227': '🌨️',
    '230': '🌨️',
    '248': '☁️ ',
    '260': '☁️ ',
    '263': '🌧️',
    '266': '🌧️',
    '281': '🌧️',
    '284': '🌧️',
    '293': '🌧️',
    '296': '🌧️',
    '299': '🌧️',
    '302': '🌧️',
    '305': '🌧️',
    '308': '🌧️',
    '311': '🌧️',
    '314': '🌧️',
    '317': '🌧️',
    '320': '🌨️',
    '323': '🌨️',
    '326': '🌨️',
    '329': '❄️ ',
    '332': '❄️ ',
    '335': '❄️ ',
    '338': '❄️ ',
    '350': '🌧️',
    '353': '🌧️',
    '356': '🌧️',
    '359': '🌧️',
    '362': '🌧️',
    '365': '🌧️',
    '368': '🌧️',
    '371': '❄️',
    '374': '🌨️',
    '377': '🌨️',
    '386': '🌨️',
    '389': '🌨️',
    '392': '🌧️',
    '395': '❄️ '
}

data = {}


weather = requests.get("https://de.wttr.in/Graz?format=j1").json()


def format_time(time):
    return time.replace("00", "").zfill(2)


def format_temp(temp):
    return (hour['FeelsLikeC']+"°").ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Nebel",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Bedeckt",
        "chanceofrain": "Regen",
        "chanceofsnow": "Schnee",
        "chanceofsunshine": "Sonnenschein",
        "chanceofthunder": "Gewitter",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

tempint = int(weather['current_condition'][0]['FeelsLikeC'])
extrachar = ''
if tempint > 0 and tempint < 10:
    extrachar = '+'


data['text'] = ' '+WEATHER_CODES[weather['current_condition'][0]['weatherCode']] + \
    " "+extrachar+weather['current_condition'][0]['FeelsLikeC']+"°"

data['tooltip'] = f"<b>{weather['current_condition'][0]['lang_de'][0]['value']} {weather['current_condition'][0]['temp_C']}°</b>\n"
data['tooltip'] += f"Gefühlt: {weather['current_condition'][0]['FeelsLikeC']}°\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']} Km/h\n"
data['tooltip'] += f"Feuchtigkeit: {weather['current_condition'][0]['humidity']}%\n"
for i, day in enumerate(weather['weather']):
    date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
    formatted_day = date_obj.strftime('%d.%m.%Y')

    sunrise_obj = datetime.strptime(day['astronomy'][0]['sunrise'], '%I:%M %p')
    formatted_sunrise = sunrise_obj.strftime('%H:%M')
    sunset_obj = datetime.strptime(day['astronomy'][0]['sunset'], '%I:%M %p')
    formatted_sunset = sunset_obj.strftime('%H:%M')

    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Heute, "
    if i == 1:
        data['tooltip'] += "Morgen, "
    data['tooltip'] += f"{formatted_day}</b>\n"
    data['tooltip'] += f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
    data['tooltip'] += f"🌅 {formatted_sunrise} 🌇 {formatted_sunset}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])} {hour['lang_de'][0]['value']}, {format_chances(hour)}\n"


print(json.dumps(data))
