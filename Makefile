
run:
	PYTHONPATH=src uvicorn src.tickethub.main:app --reload

test:
	PYTHONPATH=src APP_ENV=test pytest -v

lint:
	ruff check .

docker-build:
	docker build -f docker/Dockerfile -t tickethub .

docker-up:
	docker-compose --env-file .env -f docker/docker-compose.yml up --build

docker-down:
	docker-compose --env-file .env -f docker/docker-compose.yml down -v --remove-orphans

seed-db:
	PYTHONPATH=src python src/tickethub/db/populate_db.py

.PHONY: run test lint docker-build
