import pytest
from src.parsers.open_meteo import fetch_forecast

@pytest.mark.asyncio
async def test_real_open_meteo_daily():
    forecast = await fetch_forecast(44.12, 40.81, days=2, mode="daily")
    assert len(forecast.days) == 2
    assert forecast.days[0].temp_max is not None
    assert forecast.days[0].weather != ""

@pytest.mark.asyncio
async def test_real_open_meteo_day_parts():
    forecast = await fetch_forecast(44.12, 40.81, days=2, mode="day_parts")
    assert len(forecast.days) == 2
    day = forecast.days[0]
    assert day.morning is not None or day.evening is not None
