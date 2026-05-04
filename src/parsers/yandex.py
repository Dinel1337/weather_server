import httpx
from src.core.config import settings
from src.domain.models import ForecastResponse, DayForecast

BASE_URL = "https://api.weather.yandex.ru/v2/forecast"

async def fetch_forecast(lat: float, lon: float, days: int = 7) -> ForecastResponse:
    """Получает прогноз от Яндекс Погоды (макс 7 дней)"""
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
        # Дневная часть содержит максимум, ночная – минимум температуры
        day_part = parts["day"]
        night_part = parts["night"]
        # Используем day_short для описания погоды и ветра (более обобщённо)
        day_short = parts.get("day_short", day_part)
        days_list.append(DayForecast(
            date=forecast["date"],
            temp_max=day_part["temp_max"],
            temp_min=night_part["temp_min"],
            wind=day_short.get("wind_speed", day_part.get("wind_speed", 0)),
            prec=day_part.get("prec_mm", 0),
            weather=_translate_condition(day_short.get("condition", day_part.get("condition", "unknown")))
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
