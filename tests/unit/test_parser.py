import pytest
import re
from src.parsers.open_meteo import fetch_forecast, normalize_forecast

# Мок для daily режима
DAILY_RESPONSE = {
    "daily": {
        "time": ["2025-01-01", "2025-01-02"],
        "temperature_2m_max": [5.2, 3.8],
        "temperature_2m_min": [-1.0, -2.3],
        "wind_speed_10m_max": [12.5, 14.1],
        "precipitation_sum": [2.4, 0.0],
        "weathercode": [61, 0]
    }
}

# Мок для day_parts режима (должен содержать daily и hourly)
PARTS_RESPONSE = {
    "daily": {
        "time": ["2025-01-01"],
        "temperature_2m_max": [10],
        "temperature_2m_min": [2],
        "wind_speed_10m_max": [8.0],
        "precipitation_sum": [1.0],
        "weathercode": [61]
    },
    "hourly": {
        "time": [
            "2025-01-01T08:00",
            "2025-01-01T18:00"
        ],
        "temperature_2m": [3.5, 7.2],
        "precipitation": [0.5, 1.2],
        "weathercode": [61, 63]
    }
}

@pytest.mark.asyncio
async def test_fetch_forecast_daily(httpx_mock):
    """Open-Meteo: запрос daily режима -> ForecastResponse с днями"""
    httpx_mock.add_response(
        url=re.compile(r"https://api\.open-meteo\.com/v1/forecast.*"),
        json=DAILY_RESPONSE
    )
    data = await fetch_forecast(55.75, 37.62, days=2, mode="daily")
    assert len(data.days) == 2
    assert data.days[0].temp_max == 5.2
    assert data.days[0].weather == "небольшой дождь"
    assert data.days[1].weather == "ясно"

@pytest.mark.asyncio
async def test_fetch_forecast_day_parts(httpx_mock):
    """Open-Meteo: запрос day_parts -> карточки с morning/evening"""
    httpx_mock.add_response(
        url=re.compile(r"https://api\.open-meteo\.com/v1/forecast.*"),
        json=PARTS_RESPONSE
    )
    data = await fetch_forecast(55.75, 37.62, days=1, mode="day_parts")
    assert len(data.days) == 1
    day = data.days[0]
    assert day.morning is not None
    assert day.evening is not None
    assert day.morning.temp == 3.5
    assert day.evening.temp == 7.2
    assert day.morning.weather == "небольшой дождь"
    assert day.evening.weather == "умеренный дождь"
    assert day.morning.prec == 0.5
    assert day.evening.prec == 1.2

def test_normalize_forecast_deprecated():
    """Старый формат всё ещё работает"""
    result = normalize_forecast(DAILY_RESPONSE)
    assert len(result) == 2
    assert result[0]["temp_max"] == 5.2
    assert result[1]["weather"] == "ясно"
