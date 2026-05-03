from fastapi import APIRouter, Query
from src.services.forecast_service import get_forecast

router = APIRouter()

@router.get("/forecast")
async def forecast(
    lat: float = Query(55.75, description="Широта"),
    lon: float = Query(37.62, description="Долгота"),
    days: int = Query(10, ge=1, le=16)
):
    return await get_forecast(lat, lon, days)
