from src.core.config import settings
from src.parsers.open_meteo import fetch_forecast as open_meteo_fetch
from src.parsers.yandex import fetch_forecast as yandex_fetch
from src.domain.models import ForecastResponse

async def get_forecast(lat: float, lon: float, days: int = 10) -> ForecastResponse:
    """Фабрика: выбирает парсер в зависимости от настроек"""
    provider = settings.default_provider
    if provider == "yandex":
        return await yandex_fetch(lat, lon, days)
    return await open_meteo_fetch(lat, lon, days)
