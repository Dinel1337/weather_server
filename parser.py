import httpx

def fetch_forecast(lat: float, lon: float, days: int = 10):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,weathercode",
        "forecast_days": days,
        "timezone": "Europe/Moscow"
    }
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def normalize_forecast(data):
    codes = {0: "ясно", 61: "небольшой дождь"}
    result = []
    for i, date in enumerate(data["daily"]["time"]):
        result.append({
            "date": date,
            "temp_max": data["daily"]["temperature_2m_max"][i],
            "temp_min": data["daily"]["temperature_2m_min"][i],
            "wind": data["daily"]["wind_speed_10m_max"][i],
            "prec": data["daily"]["precipitation_sum"][i],
            "weather": codes.get(data["daily"]["weathercode"][i], "неизвестно")
        })
    return result
