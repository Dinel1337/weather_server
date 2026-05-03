import httpx
from src.domain.models import ForecastResponse, DayForecast
from src.domain.weather_code import WeatherCode

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
    for date, tmax, tmin, wind, prec, wcode in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["wind_speed_10m_max"],
        daily["precipitation_sum"],
        daily["weathercode"]
    ):
        try:
            code = WeatherCode(wcode)
            weather_str = code.description
        except ValueError:
            weather_str = "неизвестно"
        days_list.append(DayForecast(
            date=date,
            temp_max=tmax,
            temp_min=tmin,
            wind=wind,
            prec=prec,
            weather=weather_str
        ))
    return ForecastResponse(latitude=lat, longitude=lon, days=days_list)

def normalize_forecast(data: dict) -> list[dict]:
    """Deprecated: для тестов, возвращает старый формат списка словарей."""
    daily = data["daily"]
    result = []
    for date, tmax, tmin, wind, prec, wcode in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["wind_speed_10m_max"],
        daily["precipitation_sum"],
        daily["weathercode"]
    ):
        try:
            code = WeatherCode(wcode)
            weather_str = code.description
        except ValueError:
            weather_str = "неизвестно"
        result.append({
            "date": date,
            "temp_max": tmax,
            "temp_min": tmin,
            "wind": wind,
            "prec": prec,
            "weather": weather_str
        })
    return result
