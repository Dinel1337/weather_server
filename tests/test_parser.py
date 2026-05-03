import pytest  # noqa: F401
import re
from parser import fetch_forecast, normalize_forecast

RAW_RESPONSE = {
    "daily": {
        "time": ["2025-01-01", "2025-01-02"],
        "temperature_2m_max": [5.2, 3.8],
        "temperature_2m_min": [-1.0, -2.3],
        "wind_speed_10m_max": [12.5, 14.1],
        "precipitation_sum": [2.4, 0.0],
        "weathercode": [61, 0]
    }
}

def test_fetch_forecast(httpx_mock):
    # Мокаем по регулярке — любой URL с этим хостом
    httpx_mock.add_response(
        url=re.compile(r"https://api\.open-meteo\.com/v1/forecast.*"),
        json=RAW_RESPONSE
    )
    data = fetch_forecast(55.75, 37.62, days=2)
    assert "daily" in data

def test_normalize_forecast():
    result = normalize_forecast(RAW_RESPONSE)
    assert len(result) == 2
    assert result[0]["temp_max"] == 5.2
    assert result[1]["weather"] == "ясно"
