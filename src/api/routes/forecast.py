from fastapi import APIRouter, Query
from src.services.forecast_service import get_cached_forecast

router = APIRouter()

@router.get("/forecast")
async def forecast(
    lat: float = 55.75,
    lon: float = 37.62,
    days: int = 10,
    provider: str = "open_meteo",
    mode: str = Query("daily", description="daily или day_parts")
):
    return await get_cached_forecast(lat, lon, days, provider, mode)

@router.get("/open_meteo")
async def open_meteo(lat: float = 55.75, lon: float = 37.62, days: int = 10, mode: str = "daily"):
    return await get_cached_forecast(lat, lon, days, "open_meteo", mode)

@router.get("/yandex")
async def yandex(lat: float = 55.75, lon: float = 37.62, days: int = 10, mode: str = "daily"):
    return await get_cached_forecast(lat, lon, days, "yandex", mode)
