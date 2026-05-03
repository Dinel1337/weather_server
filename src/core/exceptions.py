class WeatherServiceError(Exception):
    pass

class ExternalAPIError(WeatherServiceError):
    pass
