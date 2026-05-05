from pydantic import BaseModel, Field, field_validator

class StripStringsModel(BaseModel):
    """Базовая модель: обрезает пробелы у всех строковых полей."""
    @field_validator('*', mode='before')
    @classmethod
    def strip_all_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

class ForecastRequest(StripStringsModel):
    lat: float = Field(
        default=55.75, ge=-90, le=90,
        description="Широта, от -90 до 90"
    )
    lon: float = Field(
        default=37.62, ge=-180, le=180,
        description="Долгота, от -180 до 180"
    )
    days: int = Field(
        default=10, ge=1, le=16,
        description="Количество дней прогноза (макс. 16, для Яндекс ≤7)"
    )
    provider: str = Field(
        default="open_meteo",
        description="Провайдер погоды: open_meteo или yandex"
    )
    mode: str = Field(
        default="daily",
        description=(
            "Режим отображения. daily – только суточные min/max, morning/evening будут null. "
            "day_parts – добавляет погоду на 8:00 (утро) и 18:00 (вечер) в поля morning/evening."
        )
    )
    @field_validator('provider')
    @classmethod
    def validate_provider(cls, v):
        allowed = {"open_meteo", "yandex"}
        v = v.lower()
        if v not in allowed:
            raise ValueError(f"Провайдер должен быть одним из: {allowed}")
        return v
    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v):
        allowed = {"daily", "day_parts"}
        v = v.lower()
        if v not in allowed:
            raise ValueError(f"Режим должен быть одним из: {allowed}")
        return v

class OpenMeteoRequest(StripStringsModel):
    lat: float = Field(default=55.75, ge=-90, le=90, description="Широта")
    lon: float = Field(default=37.62, ge=-180, le=180, description="Долгота")
    days: int = Field(default=10, ge=1, le=16, description="Количество дней")
    mode: str = Field(default="daily", description="daily (без утра/вечера) или day_parts (с утром/вечером)")
    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v):
        allowed = {"daily", "day_parts"}
        if v.lower() not in allowed:
            raise ValueError(f"Режим должен быть одним из: {allowed}")
        return v.lower()

class YandexRequest(StripStringsModel):
    lat: float = Field(default=55.75, ge=-90, le=90, description="Широта")
    lon: float = Field(default=37.62, ge=-180, le=180, description="Долгота")
    days: int = Field(default=7, ge=1, le=7, description="Дней (макс. 7 для Яндекса)")
    mode: str = Field(default="daily", description="daily (без утра/вечера) или day_parts (с утром/вечером)")
    @field_validator('mode')
    @classmethod
    def validate_mode(cls, v):
        allowed = {"daily", "day_parts"}
        if v.lower() not in allowed:
            raise ValueError(f"Режим должен быть одним из: {allowed}")
        return v.lower()
