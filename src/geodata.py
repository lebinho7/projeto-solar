import os
import json
import time
import logging
import requests
from geopy.geocoders import Nominatim

CACHE_DIR = os.path.join(os.getcwd(), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _cache_path(cidade): 
    safe = cidade.replace(" ", "_").replace(",", "_")
    return os.path.join(CACHE_DIR, f"geo_{safe}.json")

def get_data(cidade, refresh_cache=False):
    """Retorna (irradiacao_mensal_dict, temperatura_mensal_dict).

    Quando refresh_cache=True, ignora cache e força nova coleta.
    """
    logging.info("Buscando dados climáticos para %s", cidade)
    geo = Nominatim(user_agent="projeto_solar_geodata")
    print(f"📍 Searching for coordinates of '{cidade}'...")

    # tenta cache
    cpath = _cache_path(cidade)
    if os.path.exists(cpath) and not refresh_cache:
        try:
            with open(cpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data["irr"], data["temp"]
        except Exception:
            pass

    for _ in range(3):
        try:
            loc = geo.geocode(cidade, timeout=10)
            if not loc:
                time.sleep(1)
                continue
            logging.info("Localização encontrada: %s", loc.address)
            print(f"✅ Location found: {loc.address}")
            print("🛰️  Downloading climate data...")
            url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
            p = {
                'parameters': 'ALLSKY_SFC_SW_DWN,T2M',
                'community': 'RE',
                'longitude': loc.longitude,
                'latitude': loc.latitude,
                'format': 'JSON'
            }
            r = requests.get(url, params=p, timeout=15)
            r.raise_for_status()
            d = r.json()['properties']['parameter']
            irr = {m: d['ALLSKY_SFC_SW_DWN'][m] for m in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']}
            temp = {m: d['T2M'][m] for m in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']}
            # salva cache
            try:
                with open(cpath, "w", encoding="utf-8") as f:
                    json.dump({"irr": irr, "temp": temp}, f)
            except Exception:
                pass
            return irr, temp
        except Exception as e:
            logging.warning("Falha ao obter dados (tentativa): %s", e)
            time.sleep(1)
    return None, None
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
