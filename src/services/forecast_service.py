from src.parsers.open_meteo import fetch_forecast
from src.services.cache_service import SimpleCache
from src.domain.models import ForecastResponse

cache = SimpleCache(ttl=1800)

async def get_forecast(lat: float, lon: float, days: int = 10) -> ForecastResponse:
    key = f"{lat:.2f}:{lon:.2f}:{days}"
    cached = cache.get(key)
    if cached:
        return cached
    forecast = await fetch_forecast(lat, lon, days)
    cache.set(key, forecast)
    return forecast
