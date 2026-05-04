.PHONY: test lint tox cov view-full view-clean commit

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

tox:
	uv run tox

cov:
	uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
	echo "Отчёт: htmlcov/index.html"

ci: lint test
	echo "✅ CI пройден"

view-full:
	cat src/static/index.html

view-clean:
	grep -v '^[[:space:]]*$' src/static/index.html | grep -v '^[[:space:]]*//'

commit:
	@read -p "Введите сообщение коммита: " msg; \
	git add -A; \
	git commit -m "$$msg | added via Makefile"; \
	git push
