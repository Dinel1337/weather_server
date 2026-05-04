from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.routes import forecast, health

app = FastAPI(title="Weather Server", version="0.1.0")

# API-роуты
app.include_router(forecast.router, prefix="/api")
app.include_router(health.router, prefix="/api")

# Статика (веб-морда)
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
