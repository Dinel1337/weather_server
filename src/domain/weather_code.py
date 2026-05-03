from enum import IntEnum

class WeatherCode(IntEnum):
    CLEAR = 0
    MAINLY_CLEAR = 1
    PARTLY_CLOUDY = 2
    OVERCAST = 3
    FOG = 45
    RIME = 48
    LIGHT_DRIZZLE = 51
    MODERATE_DRIZZLE = 53
    DENSE_DRIZZLE = 55
    LIGHT_RAIN = 61
    MODERATE_RAIN = 63
    HEAVY_RAIN = 65
    LIGHT_SNOW = 71
    MODERATE_SNOW = 73
    HEAVY_SNOW = 75
    SNOW_GRAINS = 77
    SHOWER = 80
    HEAVY_SHOWER = 81
    VIOLENT_SHOWER = 82
    LIGHT_SNOW_SHOWER = 85
    HEAVY_SNOW_SHOWER = 86
    THUNDERSTORM = 95
    THUNDERSTORM_LIGHT_HAIL = 96
    THUNDERSTORM_HEAVY_HAIL = 99

    @property
    def description(self) -> str:
        """Человекочитаемое описание."""
        return _DESCRIPTIONS.get(self, "неизвестно")

_DESCRIPTIONS = {
    WeatherCode.CLEAR: "ясно",
    WeatherCode.MAINLY_CLEAR: "преимущественно ясно",
    WeatherCode.PARTLY_CLOUDY: "переменная облачность",
    WeatherCode.OVERCAST: "пасмурно",
    WeatherCode.FOG: "туман",
    WeatherCode.RIME: "иней",
    WeatherCode.LIGHT_DRIZZLE: "лёгкая морось",
    WeatherCode.MODERATE_DRIZZLE: "умеренная морось",
    WeatherCode.DENSE_DRIZZLE: "сильная морось",
    WeatherCode.LIGHT_RAIN: "небольшой дождь",
    WeatherCode.MODERATE_RAIN: "умеренный дождь",
    WeatherCode.HEAVY_RAIN: "сильный дождь",
    WeatherCode.LIGHT_SNOW: "небольшой снег",
    WeatherCode.MODERATE_SNOW: "умеренный снег",
    WeatherCode.HEAVY_SNOW: "сильный снег",
    WeatherCode.SNOW_GRAINS: "снежные зёрна",
    WeatherCode.SHOWER: "ливень",
    WeatherCode.HEAVY_SHOWER: "сильный ливень",
    WeatherCode.VIOLENT_SHOWER: "очень сильный ливень",
    WeatherCode.LIGHT_SNOW_SHOWER: "небольшой снегопад",
    WeatherCode.HEAVY_SNOW_SHOWER: "сильный снегопад",
    WeatherCode.THUNDERSTORM: "гроза",
    WeatherCode.THUNDERSTORM_LIGHT_HAIL: "гроза с небольшим градом",
    WeatherCode.THUNDERSTORM_HEAVY_HAIL: "гроза с сильным градом",
}