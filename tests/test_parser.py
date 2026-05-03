"""Интеграционный тест: проверка реального ответа Open-Meteo."""
import httpx
from parser import normalize_forecast

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
    """Дёргаем живой API и проверяем структуру."""
    resp = httpx.get(URL, params=PARAMS, timeout=10.0)
    assert resp.status_code == 200, f"Статус не 200: {resp.status_code}"
    
    data = resp.json()
    
    # Верхнеуровневые ключи
    assert "latitude" in data
    assert "longitude" in data
    assert "daily" in data
    assert "daily_units" in data
    
    daily = data["daily"]
    assert "time" in daily
    assert "temperature_2m_max" in daily
    assert "temperature_2m_min" in daily
    assert "wind_speed_10m_max" in daily
    assert "precipitation_sum" in daily
    assert "weathercode" in daily
    
    # Ровно 10 дней
    assert len(daily["time"]) == 10, f"Дней: {len(daily['time'])}, ожидалось 10"
    
    # Все массивы одной длины
    n = len(daily["time"])
    for key in ["temperature_2m_max", "temperature_2m_min", "wind_speed_10m_max", "precipitation_sum", "weathercode"]:
        assert len(daily[key]) == n, f"Массив {key} не совпадает по длине: {len(daily[key])} != {n}"
    
    # weathercode только известные
    for code in daily["weathercode"]:
        assert code in KNOWN_CODES, f"Неизвестный код погоды: {code}"
    
    # температура в разумных пределах (Земля)
    for t in daily["temperature_2m_max"]:
        assert -90 < t < 60, f"t_max за пределами: {t}"
    for t in daily["temperature_2m_min"]:
        assert -90 < t < 60, f"t_min за пределами: {t}"
    
    # осадки неотрицательные
    for p in daily["precipitation_sum"]:
        assert p >= 0, f"Осадки отрицательные: {p}"
    
    # Ветер неотрицательный
    for w in daily["wind_speed_10m_max"]:
        assert w >= 0, f"Ветер отрицательный: {w}"


def test_normalize_from_real_api():
    """normalize_forecast работает на живых данных."""
    resp = httpx.get(URL, params=PARAMS, timeout=10.0)
    data = resp.json()
    result = normalize_forecast(data)
    
    assert len(result) == 10
    for day in result:
        assert "date" in day
        assert "temp_max" in day
        assert "temp_min" in day
        assert "wind" in day
        assert "prec" in day
        assert "weather" in day
        assert isinstance(day["temp_max"], (int, float))
        assert isinstance(day["weather"], str)
