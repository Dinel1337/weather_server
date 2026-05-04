import httpx
from src.core.config import settings
from src.domain.models import ForecastResponse, DayForecast, PartForecast

BASE_URL = "https://api.weather.yandex.ru/v2/forecast"

async def fetch_forecast(lat: float, lon: float, days: int = 7, mode: str = "daily") -> ForecastResponse:
    if not settings.yandex_key:
        raise RuntimeError("YANDEX_WEATHER_KEY не задан")
    headers = {"X-Yandex-Weather-Key": settings.yandex_key}
    params = {"lat": lat, "lon": lon, "limit": min(days, 7)}
    async with httpx.AsyncClient() as client:
        resp = await client.get(BASE_URL, headers=headers, params=params, timeout=10.0)
        resp.raise_for_status()
    data = resp.json()
    days_list = []
    for forecast in data["forecasts"]:
        parts = forecast["parts"]
        day_part = parts["day"]
        night_part = parts["night"]
        day_short = parts.get("day_short", day_part)
        
        morning_data = None
        evening_data = None
        if mode == "day_parts":
            morning_raw = parts.get("morning")
            evening_raw = parts.get("evening")
            if morning_raw:
                morning_data = PartForecast(
                    temp=morning_raw["temp_avg"],
                    weather=_translate_condition(morning_raw["condition"]),
                    wind=morning_raw.get("wind_speed", 0),
                    prec=morning_raw.get("prec_mm", 0)
                )
            if evening_raw:
                evening_data = PartForecast(
                    temp=evening_raw["temp_avg"],
                    weather=_translate_condition(evening_raw["condition"]),
                    wind=evening_raw.get("wind_speed", 0),
                    prec=evening_raw.get("prec_mm", 0)
                )
        
        days_list.append(DayForecast(
            date=forecast["date"],
            temp_max=day_part["temp_max"],
            temp_min=night_part["temp_min"],
            wind=day_short.get("wind_speed", day_part.get("wind_speed", 0)),
            prec=day_part.get("prec_mm", 0),
            weather=_translate_condition(day_short.get("condition", day_part.get("condition", "unknown"))),
            morning=morning_data,
            evening=evening_data
        ))
    return ForecastResponse(latitude=lat, longitude=lon, days=days_list[:days])

def _translate_condition(condition: str) -> str:
    mapping = {
        "clear": "ясно",
        "partly-cloudy": "малооблачно",
        "cloudy": "облачно с прояснениями",
        "overcast": "пасмурно",
        "light-rain": "небольшой дождь",
        "rain": "дождь",
        "heavy-rain": "сильный дождь",
        "showers": "ливень",
        "wet-snow": "дождь со снегом",
        "light-snow": "небольшой снег",
        "snow": "снег",
        "snow-showers": "снегопад",
        "hail": "град",
        "thunderstorm": "гроза",
        "thunderstorm-with-rain": "гроза с дождём",
        "thunderstorm-with-hail": "гроза с градом",
    }
    return mapping.get(condition, condition)
