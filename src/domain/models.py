from pydantic import BaseModel
from typing import Optional

class PartForecast(BaseModel):
    temp: float
    weather: str
    wind: float
    prec: float

class DayForecast(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    wind: float
    prec: float
    weather: str
    morning: Optional[PartForecast] = None
    evening: Optional[PartForecast] = None

class ForecastResponse(BaseModel):
    latitude: float
    longitude: float
    days: list[DayForecast]
