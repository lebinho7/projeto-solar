import requests
from geopy.geocoders import Nominatim
import time

def get_coordinates(city):
    geo = Nominatim(user_agent="solar_project")
    print(f"📍 Searching for coordinates of '{city}'...")
    for _ in range(3):
        try:
            location = geo.geocode(city, timeout=10)
            if location:
                print(f"✅ Location found: {location.address}")
                return location.latitude, location.longitude
        except Exception:
            time.sleep(1)
    return None, None

def get_climate_data(latitude, longitude):
    print("🛰️  Downloading climate data...")
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN,T2M',
        'community': 'RE',
        'longitude': longitude,
        'latitude': latitude,
        'format': 'JSON'
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()['properties']['parameter']
    irradiation = data['ALLSKY_SFC_SW_DWN']
    temperature = data['T2M']
    return irradiation, temperature

def get_data(city):
    latitude, longitude = get_coordinates(city)
    if latitude is not None and longitude is not None:
        return get_climate_data(latitude, longitude)
    return None, None