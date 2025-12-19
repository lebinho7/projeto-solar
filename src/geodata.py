import os
import json
import time
import logging
import requests
from geopy.geocoders import Nominatim
from typing import Optional, Tuple, Dict

CACHE_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 dias

CACHE_DIR = os.path.join(os.getcwd(), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _cache_path(cidade): 
    safe = cidade.replace(" ", "_").replace(",", "_")
    return os.path.join(CACHE_DIR, f"geo_{safe}.json")

def clear_cache(cidade):
    """Remove o arquivo de cache para a cidade, se existir."""
    path = _cache_path(cidade)
    try:
        if os.path.exists(path):
            os.remove(path)
            logging.info("Cache removido: %s", path)
            return True
    except Exception as e:
        logging.warning("Falha ao remover cache %s: %s", path, e)
    return False

def get_nasa_data(lat: float, lon: float, timeout: int = 10) -> Optional[Dict]:
    """Obtém parâmetros climáticos da API NASA POWER com tratamento de erros.

    Retorna o dicionário de parâmetros em caso de sucesso ou None em falhas
    (sem internet, timeout, HTTP não-200, JSON inesperado, etc.).
    """
    logger = logging.getLogger(__name__)
    url = (
        "https://power.larc.nasa.gov/api/temporal/climatology/point"
    )
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON",
    }
    try:
        print(f"📡 Conectando com satélite NASA em ({lat:.4f}, {lon:.4f})...")
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
        return payload["properties"]["parameter"]
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Sem conexão com a internet.")
        logger.warning("Conexão indisponível ao acessar NASA POWER")
        return None
    except requests.exceptions.Timeout:
        print("❌ ERRO: O servidor da NASA demorou demais para responder.")
        logger.warning("Timeout ao acessar NASA POWER")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ ERRO HTTP ao acessar NASA: {e}")
        logger.warning("HTTPError NASA POWER: %s", e)
        return None
    except (KeyError, ValueError) as e:
        print("❌ ERRO: Resposta inesperada da NASA.")
        logger.warning("Resposta JSON inesperada: %s", e)
        return None
    except Exception as e:
        print(f"❌ ERRO DESCONHECIDO: {e}")
        logger.warning("Erro inesperado NASA POWER: %s", e)
        return None

def get_data(cidade, refresh_cache=False, ttl_seconds=CACHE_TTL_SECONDS, allow_stale_fallback=True, retries: int = 3, nasa_timeout: int = 15):
    """Retorna (irradiacao_mensal_dict, temperatura_mensal_dict).

    Quando refresh_cache=True, ignora cache e força nova coleta.
    """
    logger = logging.getLogger(__name__)
    logger.info("Buscando dados climáticos para %s", cidade)
    geo = Nominatim(user_agent="projeto_solar_geodata")
    print(f"📍 Searching for coordinates of '{cidade}'...")

    # Normaliza TTL: None usa padrão; 0 = cache infinito (nunca expira)
    if ttl_seconds is None:
        ttl = CACHE_TTL_SECONDS
    else:
        ttl = ttl_seconds

    # tenta cache
    cpath = _cache_path(cidade)
    stale_payload = None
    stale_age_days = None
    if os.path.exists(cpath) and not refresh_cache:
        try:
            with open(cpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            now = time.time()
            ts = data.get("ts")
            if ts is None:
                try:
                    ts = os.path.getmtime(cpath)
                except Exception:
                    ts = now
            age = now - ts
            # TTL == 0 -> cache infinito
            if ttl == 0 or age <= ttl:
                age_days = age/86400.0
                if ttl == 0:
                    print(f"ℹ️  Usando cache (infinito), idade {age_days:.1f} dias.")
                else:
                    ttl_days = ttl/86400.0
                    print(f"ℹ️  Usando cache com idade de {age_days:.1f} dias (TTL {ttl_days:.0f} dias).")
                return data["irr"], data["temp"]
            else:
                stale_age_days = age/86400.0
                logger.info("Cache expirado (%.1f dias). Requisitando novos dados...", stale_age_days)
                stale_payload = (data["irr"], data["temp"])  # para fallback
        except Exception:
            pass

    for _ in range(max(0, int(retries)) or 1):
        try:
            loc = geo.geocode(cidade, timeout=10)
            if not loc:
                time.sleep(1)
                continue
            logger.info("Localização encontrada: %s", loc.address)
            print(f"✅ Location found: {loc.address}")
            print("🛰️  Downloading climate data...")

            d = get_nasa_data(lat=loc.latitude, lon=loc.longitude, timeout=nasa_timeout)
            if d is None:
                # tentar novamente; pode ter sido falha transitória
                time.sleep(1)
                continue

            irr = {m: d['ALLSKY_SFC_SW_DWN'][m] for m in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']}
            temp = {m: d['T2M'][m] for m in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']}
            # salva cache
            try:
                with open(cpath, "w", encoding="utf-8") as f:
                    json.dump({"irr": irr, "temp": temp, "ts": time.time()}, f)
            except Exception:
                pass
            return irr, temp
        except Exception as e:
            logger.warning("Falha ao geocodificar/obter dados (tentativa): %s", e)
            time.sleep(1)
    # fallback para cache vencido se permitido
    if allow_stale_fallback and stale_payload is not None:
        if stale_age_days is not None:
            print(f"⚠️  Usando cache vencido de {stale_age_days:.1f} dias por indisponibilidade de rede.")
        logger.warning("Usando cache vencido por indisponibilidade de rede (%.1f dias).", stale_age_days or -1)
        return stale_payload
    return None, None
 
