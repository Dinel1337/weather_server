from src.parsers import get_forecast
from src.services.cache_service import SimpleCache
from src.domain.models import ForecastResponse

cache = SimpleCache(ttl=3600)

async def get_cached_forecast(lat: float, lon: float, days: int = 10) -> ForecastResponse:
    # Округление координат до сетки ~11 км
    grid_lat = round(lat, 1)
    grid_lon = round(lon, 1)
    key = f"{grid_lat}:{grid_lon}:{days}"
    if (cached := cache.get(key)) is not None:
        return cached
    forecast = await get_forecast(grid_lat, grid_lon, days)
    cache.set(key, forecast)
    return forecast
