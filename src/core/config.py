from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cache_ttl: int = 1800
    api_host: str = "0.0.0.0"
    api_port: int = 8000

settings = Settings()
