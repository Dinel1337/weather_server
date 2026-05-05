#!/bin/bash
# setup.sh — автоустановка Weather Server (клон → установка → запуск)
# Запуск: curl -sSL https://raw.githubusercontent.com/Dinel1337/weather_server/master/bin/setup.sh | bash

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Weather Server — установка и автозапуск           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Python
echo -e "${YELLOW}→ Проверка Python 3.13...${NC}"
if ! command -v python3.13 &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3.13 не найден.${NC}"
    echo -e "   Установите: https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✓ Python установлен${NC}"

# 2. uv
echo -e "${YELLOW}→ Проверка uv...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}📦 Установка uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi
echo -e "${GREEN}✓ uv установлен${NC}"

# 3. Git
echo -e "${YELLOW}→ Проверка Git...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git не найден. Установите git${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git установлен${NC}"

# 4. Клонирование (если ещё не в папке проекта)
if [ ! -f "pyproject.toml" ]; then
    echo -e "${YELLOW}→ Клонирование репозитория...${NC}"
    git clone https://github.com/Dinel1337/weather_server.git
    cd weather_server
else
    echo -e "${GREEN}✓ Уже в репозитории weather_server${NC}"
fi

# 5. .env
echo -e "${YELLOW}→ Настройка .env...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << 'DOTENV'
yandex_weather_key=33a7cea3-6b42-4722-ae45-3f31246c00db
weather_provider=open_meteo
cache_ttl=3600
DOTENV
    echo -e "${GREEN}✓ .env создан${NC}"
else
    echo -e "${GREEN}✓ .env уже существует${NC}"
fi

# 6. Зависимости
echo -e "${YELLOW}→ Установка зависимостей...${NC}"
uv sync
echo -e "${GREEN}✓ Зависимости установлены${NC}"

# 7. Автозапуск сервера
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✅ Всё готово! Запускаем сервер...           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🌐 Веб-интерфейс откроется по адресу:${NC} ${GREEN}http://localhost:8000${NC}"
echo -e "${BLUE}📚 Документация API:${NC} ${GREEN}http://localhost:8000/docs${NC}"
echo -e "${BLUE}🛑 Чтобы остановить сервер, нажмите Ctrl+C${NC}"
echo ""

# Запускаем сервер в текущей папке (интерактивно, вывод в терминал)
uv run uvicorn src.main:app --reload
