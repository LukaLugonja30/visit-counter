.PHONY: build up down test logs health

build:
	docker compose build
up:
	docker compose up -d --build
down:
	docker compose down
test:
	ruff check .
	pytest -v
logs:
	docker compose logs -f app
health:
	./scripts/healthcheck.sh http://localhost:8080