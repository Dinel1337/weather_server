import pytest
from src.parsers.yandex import fetch_forecast
from src.core.config import settings

@pytest.mark.skipif(not settings.yandex_key, reason="YANDEX_WEATHER_KEY не задан")
@pytest.mark.asyncio
async def test_yandex_real():
    forecast = await fetch_forecast(44.12, 40.81, days=2)
    assert len(forecast.days) == 2
