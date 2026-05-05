# Weather Server

Парсер погоды для ESP32. Принимает координаты, отдаёт прогноз на 10 дней в формате JSON.  
Источник данных — [Open-Meteo](https://open-meteo.com/).

## Стек технологий

- Python 3.11+
- FastAPI
- httpx
- Pydantic
- pytest + pytest-httpx
- uv (управление зависимостями)
- Uvicorn (ASGI сервер)

## Быстрая установка (одной командой)

```bash
curl -sSL https://raw.githubusercontent.com/Dinel1337/weather_server/main/bin/setup.sh | bash
```
## Установка

```bash
git clone https://github.com/Dinel1337/weather_server.git
cd weather_server
uv sync
```

## API

### `GET /forecast`

#### Параметры запроса

| Параметр | Тип    | Обязательный | По умолчанию | Описание          |
|----------|--------|--------------|--------------|-------------------|
| `lat`    | float  | ✅ да         | —            | Широта            |
| `lon`    | float  | ✅ да         | —            | Долгота           |
| `days`   | int    | ❌ нет        | 10           | Количество дней   |

#### Пример ответа

```json
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
```
## Кэширование

Прогноз кэшируется на **30 минут**.  
При повторном запросе с теми же координатами Open-Meteo не вызывается.
## Структура проекта
```
weather_server/
├── main.py          # FastAPI-сервер
├── parser.py        # Запрос к Open-Meteo, нормализация данных
├── cache.py         # Кэш в памяти с TTL
├── models.py        # Pydantic-схемы
├── tests/
│   └── test_parser.py  # Тесты парсера
├── pyproject.toml
└── README.md
```

## Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешный ответ |
| 422 | Ошибка валидации (некорректные lat/lon или days) |
| 500 | Ошибка сервера или таймаут Open-Meteo |