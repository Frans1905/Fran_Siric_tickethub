
run:
	PYTHONPATH=src uvicorn src.tickethub.main:app --reload

test:
	PYTHONPATH=src pytest -v

lint:
	ruff check .

docker-build:
	docker build -f docker/Dockerfile -t tickethub .

docker-up:
	docker-compose -f docker/docker-compose.yml up --build

.PHONY: run test lint docker-build
