import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    yandex_key: str = os.getenv("YANDEX_WEATHER_KEY", "")
    default_provider: str = os.getenv("WEATHER_PROVIDER", "open_meteo")  # open_meteo или yandex
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))

settings = Settings()
