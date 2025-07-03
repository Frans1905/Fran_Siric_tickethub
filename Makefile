
run:
	PYTHONPATH=src uvicorn src.tickethub.main:app --reload

test:
	PYTHONPATH=src pytest -v

lint:
	ruff check .

docker-build:
	docker build -t tickethub .

.PHONY: run test lint docker-build
