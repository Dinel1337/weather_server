from pydantic import BaseModel, Field
from typing import Optional

class PartForecast(BaseModel):
    temp: float = Field(..., description="Температура (°C) в указанное время")
    weather: str = Field(..., description="Описание погоды (облачно, дождь и т.п.)")
    wind: float = Field(..., description="Скорость ветра (м/с)")
    prec: float = Field(..., description="Количество осадков (мм)")
    model_config = {
        "json_schema_extra": {
            "example": {"temp": 14.2, "weather": "переменная облачность", "wind": 3.1, "prec": 0.0}
        }
    }

class DayForecast(BaseModel):
    date: str = Field(..., description="Дата в формате YYYY-MM-DD")
    temp_max: float = Field(..., description="Максимальная температура за день (°C)")
    temp_min: float = Field(..., description="Минимальная температура за ночь (°C)")
    wind: float = Field(..., description="Максимальная скорость ветра (м/с)")
    prec: float = Field(..., description="Сумма осадков за день (мм)")
    weather: str = Field(..., description="Общее описание погоды на день")
    morning: Optional[PartForecast] = Field(
        None,
        description="Погода на 8:00 утра. Заполняется только при mode=day_parts."
    )
    evening: Optional[PartForecast] = Field(
        None,
        description="Погода на 18:00 (вечер). Заполняется только при mode=day_parts."
    )
    model_config = {
        "json_schema_extra": {
            "example": {
                "date": "2025-05-04",
                "temp_max": 24.4,
                "temp_min": 11.5,
                "wind": 11.2,
                "prec": 0.0,
                "weather": "пасмурно",
                "morning": {"temp": 14.2, "weather": "переменная облачность", "wind": 3.1, "prec": 0.0},
                "evening": {"temp": 20.8, "weather": "небольшой дождь", "wind": 4.0, "prec": 1.2}
            }
        }
    }

class ForecastResponse(BaseModel):
    latitude: float = Field(..., description="Широта запроса")
    longitude: float = Field(..., description="Долгота запроса")
    days: list[DayForecast] = Field(..., description="Массив дней с прогнозом")
    model_config = {
        "json_schema_extra": {
            "example": {
                "latitude": 55.75,
                "longitude": 37.62,
                "days": [
                    {
                        "date": "2025-05-04",
                        "temp_max": 24.4,
                        "temp_min": 11.5,
                        "wind": 11.2,
                        "prec": 0.0,
                        "weather": "пасмурно",
                        "morning": {"temp": 14.2, "weather": "переменная облачность", "wind": 3.1, "prec": 0.0},
                        "evening": {"temp": 20.8, "weather": "небольшой дождь", "wind": 4.0, "prec": 1.2}
                    }
                ]
            }
        }
    }
