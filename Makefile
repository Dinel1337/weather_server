.PHONY: test lint tox

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

tox:
	uv run tox

ci: lint test
	echo "✅ CI пройден"
