from fastapi import APIRouter, Depends
from src.services.forecast_service import get_cached_forecast
from src.domain.request_models import ForecastRequest, OpenMeteoRequest, YandexRequest

router = APIRouter()

@router.get("/forecast")
async def forecast(params: ForecastRequest = Depends()):
    return await get_cached_forecast(
        lat=params.lat,
        lon=params.lon,
        days=params.days,
        provider=params.provider,
        mode=params.mode
    )

@router.get("/open_meteo")
async def open_meteo(params: OpenMeteoRequest = Depends()):
    return await get_cached_forecast(
        lat=params.lat,
        lon=params.lon,
        days=params.days,
        provider="open_meteo",
        mode=params.mode
    )

@router.get("/yandex")
async def yandex(params: YandexRequest = Depends()):
    return await get_cached_forecast(
        lat=params.lat,
        lon=params.lon,
        days=params.days,
        provider="yandex",
        mode=params.mode
    )
