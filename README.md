
Weather Server
Парсер погоды для ESP32. Принимает координаты, отдаёт прогноз на 10 дней в JSON. Источник данных — Open-Meteo.

Стек
Python 3.11+

FastAPI

httpx

Pydantic

pytest + pytest-httpx

Установка
git clone https://github.com/Dinel1337/weather_server.git
cd weather_server
uv sync

Запуск
uv run uvicorn main:app --host 0.0.0.0 --port 8000

API
GET /forecast

Параметры:

lat (float, обязательно) — широта

lon (float, обязательно) — долгота

days (int, опционально, по умолчанию 10)

Пример запроса: http://localhost:8000/forecast?lat=55.75&lon=37.62&days=3

Пример ответа:
{
"latitude": 55.75,
"longitude": 37.62,
"days": [
{
"date": "2025-01-01",
"temp_max": 5.2,
"temp_min": -1.0,
"wind": 12.5,
"prec": 2.4,
"weather": "небольшой дождь"
}
]
}

Тесты
uv run pytest tests/ -v

Кэш
Прогноз кэшируется на 30 минут. При повторном запросе тех же координат Open-Meteo не дёргается.

Структура
weather_server/
main.py — FastAPI-сервер
parser.py — Запрос к Open-Meteo, нормализация
cache.py — Кэш в памяти с TTL
models.py — Pydantic-схемы
tests/
test_parser.py — Тесты парсера
pyproject.toml
README.md
