from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
    
    yandex_weather_key: str = ""
    weather_provider: str = "open_meteo"
    cache_ttl: int = 3600

    @property
    def yandex_key(self) -> str:
        return self.yandex_weather_key

settings = Settings()
