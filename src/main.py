import sys
from pathlib import Path

# Добавляем корень проекта в путь для импортов src.*
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.api.routes import forecast, health
from src.core.exceptions import WeatherServiceError, ExternalAPIError

app = FastAPI(
    title="Weather Server",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS для возможных веб-клиентов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры API
app.include_router(forecast.router, prefix="/api")
app.include_router(health.router, prefix="/api")

# Подключение статики (фронтенд)
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

# Обработчики кастомных исключений
@app.exception_handler(WeatherServiceError)
async def weather_service_error_handler(request: Request, exc: WeatherServiceError):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )

@app.exception_handler(ExternalAPIError)
async def external_api_error_handler(request: Request, exc: ExternalAPIError):
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )
