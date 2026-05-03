import httpx
from src.domain.models import ForecastResponse, DayForecast
from src.domain.weather_code import WMO_CODES

async def fetch_forecast(lat: float, lon: float, days: int = 10) -> ForecastResponse:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,weathercode",
        "forecast_days": days,
        "timezone": "Europe/Moscow"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
    data = resp.json()
    daily = data["daily"]
    days_list = []
    for i, date in enumerate(daily["time"]):
        code = daily["weathercode"][i]
        days_list.append(DayForecast(
            date=date,
            temp_max=daily["temperature_2m_max"][i],
            temp_min=daily["temperature_2m_min"][i],
            wind=daily["wind_speed_10m_max"][i],
            prec=daily["precipitation_sum"][i],
            weather=WMO_CODES.get(code, "неизвестно")
        ))
    return ForecastResponse(latitude=lat, longitude=lon, days=days_list)

def normalize_forecast(data: dict) -> list[dict]:
    """Deprecated: для тестов, возвращает старый формат списка словарей."""
    daily = data["daily"]
    result = []
    for i, date in enumerate(daily["time"]):
        code = daily["weathercode"][i]
        result.append({
            "date": date,
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "wind": daily["wind_speed_10m_max"][i],
            "prec": daily["precipitation_sum"][i],
            "weather": WMO_CODES.get(code, "неизвестно")
        })
    return result
