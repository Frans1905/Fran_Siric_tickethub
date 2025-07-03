
# README.md

````markdown
# TicketHub

**TicketHub** is a FastAPI-based middleware REST service that fetches and exposes support tickets from an external API (DummyJSON).

## Features

- List tickets with pagination, filtering, and search
- Fetch ticket details with transformed model + raw source payload
- Async HTTP calls via httpx
- Input validation & serialization with Pydantic
- Unit & integration tests (pytest + httpx.MockTransport)

## Tech Stack

- Python 3.11+ (typing, async/await)
- FastAPI 0.111
- httpx 0.27
- Pydantic 2.7
- pytest
- Docker & Docker Compose

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized setup)

## Setup

1. **Clone the repo**
   ```bash
   git clone git@github.com:Frans1905/tickethub.git
   cd tickethub
````

2. **Create a virtual environment**

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**

   ```bash
   # From project root
   make run
   # or
   PYTHONPATH=./src uvicorn tickethub.main:app --reload
   ```

5. **Interactive API docs**

   * Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * ReDoc:      [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing

```bash
pytest -v
```

## Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## Environment Variables

Override defaults by creating a `.env` file:

```dotenv
# Example
EXTERNAL_API_URL=https://dummyjson.com
CACHE_TTL=300
```

## Project Structure

```
├── src/
│   └── tickethub/      # application code
├── tests/              # pytest test suite
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

## CI/CD

A GitHub Actions workflow is configured under `.github/workflows/ci.yml` to:

* Run linting (ruff)
* Run pytest
* Build Docker image

```
