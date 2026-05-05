.PHONY: test lint tox cov view-full view-clean commit
run:
	uv run uvicorn src.main:app --reload
test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

tox:
	uv run tox

cov:
	uv run pytest tests/ --cov=src --cov-report=term-missing

copy:
	bash bin/\!copyTreeProject.bash

ci: lint test
	echo "✅ CI пройден"

commit:
	@read -p "Введите сообщение коммита: " msg; \
	git add -A; \
	git commit -m "$$msg | added via Makefile"; \
	git push
