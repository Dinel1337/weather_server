import pytest
from src.parsers.yandex import fetch_forecast
from src.core.config import settings

@pytest.mark.skipif(not settings.yandex_key, reason="yandex_weather_key не задан")
@pytest.mark.asyncio
async def test_real_yandex_daily():
    forecast = await fetch_forecast(44.12, 40.81, days=2, mode="daily")
    assert len(forecast.days) == 2

@pytest.mark.skipif(not settings.yandex_key, reason="yandex_weather_key не задан")
@pytest.mark.asyncio
async def test_real_yandex_day_parts():
    forecast = await fetch_forecast(44.12, 40.81, days=2, mode="day_parts")
    assert len(forecast.days) == 2
    day = forecast.days[0]
    assert day.morning is not None or day.evening is not None
