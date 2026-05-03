from pydantic import BaseModel

class DayForecast(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    wind: float
    prec: float
    weather: str

class ForecastResponse(BaseModel):
    latitude: float
    longitude: float
    days: list[DayForecast]
