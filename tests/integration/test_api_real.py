import httpx
from src.parsers.open_meteo import normalize_forecast

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 55.75,
    "longitude": 37.62,
    "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,weathercode",
    "forecast_days": 10,
    "timezone": "Europe/Moscow"
}
KNOWN_CODES = {0, 1, 2, 3, 45, 48, 51, 53, 55, 56, 57, 61, 63, 65, 66, 67,
               71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 99}

def test_real_api_response():
    resp = httpx.get(URL, params=PARAMS, timeout=10.0)
    assert resp.status_code == 200
    data = resp.json()
    daily = data["daily"]
    assert len(daily["time"]) == 10
    for code in daily["weathercode"]:
        assert code in KNOWN_CODES
    for t in daily["temperature_2m_max"]:
        assert -90 < t < 60
    for p in daily["precipitation_sum"]:
        assert p >= 0

def test_normalize_from_real_api():
    resp = httpx.get(URL, params=PARAMS, timeout=10.0)
    result = normalize_forecast(resp.json())
    assert len(result) == 10
    for day in result:
        assert all(k in day for k in ("date", "temp_max", "temp_min", "wind", "prec", "weather"))
