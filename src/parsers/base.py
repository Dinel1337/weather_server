from abc import ABC, abstractmethod
from src.domain.models import ForecastResponse

class BaseWeatherParser(ABC):
    @abstractmethod
    async def fetch(self, lat: float, lon: float, days: int = 10) -> ForecastResponse:
        ...
