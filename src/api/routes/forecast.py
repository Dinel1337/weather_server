from fastapi import APIRouter, Depends
from src.services.forecast_service import get_cached_forecast
from src.domain.request_models import ForecastRequest, OpenMeteoRequest, YandexRequest
from src.domain.models import ForecastResponse

router = APIRouter(tags=["Прогноз"])

@router.get(
    "/forecast",
    response_model=ForecastResponse,
    summary="Получить прогноз погоды",
    description="""Возвращает прогноз на указанное количество дней (до 16 для Open-Meteo, до 7 для Яндекс).

**Источники:**
- Open-Meteo: `https://api.open-meteo.com/v1/forecast` (бесплатно, без ключа)
- Яндекс: `https://api.weather.yandex.ru/v2/forecast` (требуется API-ключ в `.env`)

**Режимы и как меняется ответ:**
- `mode=daily` – только суточные минимумы/максимумы. Поля `morning` и `evening` будут `null`.
- `mode=day_parts` – добавляются блоки `morning` (на 8:00) и `evening` (на 18:00) с температурой, осадками и описанием.
"""
)
async def forecast(params: ForecastRequest = Depends()):
    return await get_cached_forecast(
        lat=params.lat, lon=params.lon, days=params.days,
        provider=params.provider, mode=params.mode
    )

@router.get(
    "/open_meteo",
    response_model=ForecastResponse,
    summary="Прогноз Open-Meteo",
    description="Прямой вызов Open-Meteo. Бесплатный API, не требует ключа. Режимы `daily` и `day_parts` работают одинаково."
)
async def open_meteo(params: OpenMeteoRequest = Depends()):
    return await get_cached_forecast(
        lat=params.lat, lon=params.lon, days=params.days,
        provider="open_meteo", mode=params.mode
    )

@router.get(
    "/yandex",
    response_model=ForecastResponse,
    summary="Прогноз Яндекс",
    description="Прямой вызов Яндекс Погоды. Требует ключ в `yandex_weather_key`. Режимы `daily` и `day_parts` работают одинаково."
)
async def yandex(params: YandexRequest = Depends()):
    return await get_cached_forecast(
        lat=params.lat, lon=params.lon, days=params.days,
        provider="yandex", mode=params.mode
    )
