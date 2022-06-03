from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
# from .models import Location
import json


def get_photo(state, city):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "per_page": 1,
        "query": f"{city} {state}"
    }
    url = "https://api.pexels.com/v1/search"
    res = requests.get(url, params=params, headers=headers)
    content = json.loads(res.content)
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(state, city):
    params = {
        "q": f"{city}, {state},US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = "http://api.openweathermap.org/geo/1.0/direct"
    res = requests.get(url, params=params)
    content = json.loads(res.content)
    try:
        latitude = content[0]["lat"]
        longitude = content[0]["lon"]
    except (KeyError, IndexError):
        return None
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": "bb65350d446bbf728ae5b44a904487aa",
        "units": "imperial",
    }
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    res = requests.get(geo_url, params=params)
    content = json.loads(res.content)

    try:
        return{
            "description": content["weather"][0]["description"],
            "temp": content["main"]["temp"],
        }
    except (KeyError, IndexError):
        return None
#     def get_weather_data(state, city):
#     geo_url = "http://api.openweathermap.org/geo/1.0/direct"
#     params = {
#         "q": f"{city}, {state}, US",
#         "limit": 1,
#         "appid": "bb65350d446bbf728ae5b44a904487aa",
#     }
#     res = requests.get(geo_url, params=params)
#     content = json.loads(res.content)
#     lattitude = getattr({content}, {"lat"})
#     longitude = getattr({content}, {"lon"})
#     return content
# print(get_weather_data(state, city))
