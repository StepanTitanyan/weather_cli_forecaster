import json
import time
from pathlib import Path

CACHE_FILE = Path("cache/weather_cache.json")
CACHE_SECONDS = 600


def load_cache():
    if not CACHE_FILE.exists():
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache):
    CACHE_FILE.parent.mkdir(exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=4)


def get_from_cache(cache_key):
    cache = load_cache()

    if cache_key not in cache:
        return None

    cached_item = cache[cache_key]
    cached_time = cached_item.get("time")

    if time.time() - cached_time > CACHE_SECONDS:
        return None

    return cached_item.get("data")


def save_to_cache(cache_key, data):
    cache = load_cache()
    cache[cache_key] = {"time": time.time(), "data": data}
    save_cache(cache)
