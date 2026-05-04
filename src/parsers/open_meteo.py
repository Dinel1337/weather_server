import httpx
from src.domain.models import ForecastResponse, DayForecast, PartForecast
from src.domain.weather_code import WeatherCode
from datetime import datetime
from collections import defaultdict

async def fetch_forecast(lat: float, lon: float, days: int = 10, mode: str = "daily") -> ForecastResponse:
    url = "https://api.open-meteo.com/v1/forecast"
    base_params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "Europe/Moscow",
        "forecast_days": days
    }
    
    if mode == "day_parts":
        # Запрашиваем и daily, и hourly
        params = {
            **base_params,
            "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,weathercode",
            "hourly": "temperature_2m,precipitation,weathercode"
        }
    else:
        params = {
            **base_params,
            "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,weathercode"
        }
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
    data = resp.json()
    
    if mode == "day_parts":
        hourly = data["hourly"]
        times = hourly["time"]
        temperatures = hourly["temperature_2m"]
        precipitations = hourly["precipitation"]
        codes = hourly["weathercode"]
        
        # Группируем по дням и выбираем значения на 8:00 и 18:00
        day_hours = defaultdict(lambda: {"8": None, "18": None})
        
        for i, t_str in enumerate(times):
            dt = datetime.fromisoformat(t_str)
            day = dt.date().isoformat()
            if dt.hour == 8:
                day_hours[day]["8"] = {
                    "temp": temperatures[i],
                    "prec": precipitations[i],
                    "code": codes[i]
                }
            elif dt.hour == 18:
                day_hours[day]["18"] = {
                    "temp": temperatures[i],
                    "prec": precipitations[i],
                    "code": codes[i]
                }
        
        daily_data = data["daily"]
        days_list = []
        for i, day_str in enumerate(daily_data["time"]):
            morning = day_hours[day_str]["8"]
            evening = day_hours[day_str]["18"]
            
            morning_part = None
            if morning:
                try:
                    wcode = WeatherCode(morning["code"])
                    weather_str = wcode.description
                except ValueError:
                    weather_str = "неизвестно"
                morning_part = PartForecast(
                    temp=morning["temp"],
                    weather=weather_str,
                    wind=0.0,  # в hourly нет ветра
                    prec=morning["prec"]
                )
            
            evening_part = None
            if evening:
                try:
                    wcode = WeatherCode(evening["code"])
                    weather_str = wcode.description
                except ValueError:
                    weather_str = "неизвестно"
                evening_part = PartForecast(
                    temp=evening["temp"],
                    weather=weather_str,
                    wind=0.0,
                    prec=evening["prec"]
                )
            
            days_list.append(DayForecast(
                date=day_str,
                temp_max=daily_data["temperature_2m_max"][i],
                temp_min=daily_data["temperature_2m_min"][i],
                wind=daily_data["wind_speed_10m_max"][i],
                prec=daily_data["precipitation_sum"][i],
                weather=WeatherCode(daily_data["weathercode"][i]).description,
                morning=morning_part,
                evening=evening_part
            ))
        return ForecastResponse(latitude=lat, longitude=lon, days=days_list)
    
    # Режим daily
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
    """Deprecated: для тестов"""
    daily = data["daily"]
    result = []
    for date, tmax, tmin, wind, prec, wcode in zip(
        daily["time"], daily["temperature_2m_max"], daily["temperature_2m_min"],
        daily["wind_speed_10m_max"], daily["precipitation_sum"], daily["weathercode"]
    ):
        try:
            code = WeatherCode(wcode)
            weather_str = code.description
        except ValueError:
            weather_str = "неизвестно"
        result.append({
            "date": date, "temp_max": tmax, "temp_min": tmin,
            "wind": wind, "prec": prec, "weather": weather_str
        })
    return result
