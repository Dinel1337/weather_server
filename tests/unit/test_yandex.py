import pytest
import re
from src.parsers.yandex import fetch_forecast

# Мок ответа Яндекса для daily режима
YANDEX_DAILY = {
    "forecasts": [
        {
            "date": "2026-05-10",
            "parts": {
                "day_short": {"temp": 18, "wind_speed": 3.4, "condition": "light-rain"},
                "day": {"temp_max": 20, "prec_mm": 2.5, "wind_speed": 3.4},
                "night": {"temp_min": 10}
            }
        }
    ]
}

# Мок ответа Яндекса для day_parts режима
YANDEX_PARTS = {
    "forecasts": [
        {
            "date": "2026-05-11",
            "parts": {
                "day_short": {"temp": 22, "wind_speed": 5.1, "condition": "clear"},
                "day": {"temp_max": 24, "prec_mm": 0, "wind_speed": 5.1},
                "night": {"temp_min": 12},
                "morning": {"temp_avg": 15, "condition": "cloudy", "wind_speed": 2.0, "prec_mm": 0.0},
                "evening": {"temp_avg": 18, "condition": "rain", "wind_speed": 3.0, "prec_mm": 1.5}
            }
        }
    ]
}

@pytest.mark.asyncio
async def test_yandex_daily(httpx_mock, monkeypatch):
    """Яндекс: daily режим -> макс./мин. температуры, описание"""
    # Подменяем поле yandex_weather_key (основа property yandex_key)
    monkeypatch.setattr("src.parsers.yandex.settings.yandex_weather_key", "fake-key")
    httpx_mock.add_response(
        url=re.compile(r"https://api\.weather\.yandex\.ru/v2/forecast.*"),
        json=YANDEX_DAILY
    )
    result = await fetch_forecast(55.75, 37.62, days=1, mode="daily")
    assert len(result.days) == 1
    day = result.days[0]
    assert day.temp_max == 20
    assert day.temp_min == 10
    assert day.weather == "небольшой дождь"
    assert day.wind == 3.4
    assert day.prec == 2.5

@pytest.mark.asyncio
async def test_yandex_day_parts(httpx_mock, monkeypatch):
    """Яндекс: day_parts режим -> утро/вечер заполнены"""
    monkeypatch.setattr("src.parsers.yandex.settings.yandex_weather_key", "fake-key")
    httpx_mock.add_response(
        url=re.compile(r"https://api\.weather\.yandex\.ru/v2/forecast.*"),
        json=YANDEX_PARTS
    )
    result = await fetch_forecast(55.75, 37.62, days=1, mode="day_parts")
    day = result.days[0]
    assert day.morning is not None
    assert day.evening is not None
    assert day.morning.temp == 15
    assert day.morning.weather == "облачно с прояснениями"
    assert day.evening.temp == 18
    assert day.evening.weather == "дождь"
    assert day.evening.prec == 1.5
