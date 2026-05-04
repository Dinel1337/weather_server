import pytest
import re
from src.parsers.yandex import fetch_forecast

YANDEX_RESPONSE = {
    "forecasts": [
        {
            "date": "2026-05-10",
            "parts": {
                "day_short": {"temp": 18, "wind_speed": 3.4, "condition": "light-rain"},
                "day": {"temp_max": 20, "prec_mm": 2.5, "wind_speed": 3.4},
                "night": {"temp_min": 10}
            }
        },
        {
            "date": "2026-05-11",
            "parts": {
                "day_short": {"temp": 22, "wind_speed": 5.1, "condition": "clear"},
                "day": {"temp_max": 24, "prec_mm": 0, "wind_speed": 5.1},
                "night": {"temp_min": 12}
            }
        }
    ]
}

@pytest.mark.asyncio
async def test_yandex_fetch(monkeypatch, httpx_mock):
    monkeypatch.setattr("src.parsers.yandex.settings.yandex_key", "test_key")
    httpx_mock.add_response(
        url=re.compile(r"https://api\.weather\.yandex\.ru/v2/forecast.*"),
        json=YANDEX_RESPONSE
    )
    result = await fetch_forecast(55.75, 37.62, days=2)
    assert result.latitude == 55.75
    assert len(result.days) == 2
    # Теперь проверяем правильные поля
    assert result.days[0].temp_max == 20
    assert result.days[0].temp_min == 10
    assert result.days[0].wind == 3.4
    assert result.days[0].prec == 2.5
    assert result.days[0].weather == "небольшой дождь"
    assert result.days[1].temp_max == 24
    assert result.days[1].weather == "ясно"
