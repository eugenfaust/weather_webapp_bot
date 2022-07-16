import requests
from typing import Optional
from main_config import WEATHER_GEOCODING_URL, WEATHER_GEODECODING_URL


def get_location_by_name(name: str) -> Optional[dict]:
    result = requests.get(WEATHER_GEOCODING_URL.format(name)).json()
    if result['cod'] == '404':
        return None
    else:
        data = {'lon': result['coord']['lon'], 'lat': result['coord']['lat'], 'city_name': name}
        return data


def get_location_by_coord(lat: str, lon: str) -> Optional[dict]:
    result = requests.get(WEATHER_GEODECODING_URL.format(lat, lon)).json()
    if len(result) == 0:
        return None
    else:
        return {'lon': lon, 'lat': lat, 'city_name': result[0]['local_names']['ru']}