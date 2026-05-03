from fastapi import FastAPI
from src.api.routes import forecast, health

app = FastAPI(title="Weather Server", version="0.1.0")
app.include_router(forecast.router, prefix="/api")
app.include_router(health.router, prefix="/api")
