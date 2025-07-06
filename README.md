
# TicketHub

**TicketHub** is a FastAPI-based middleware service for aggregating and exposing support tickets from an external API (DummyJSON).

---

## 🚀 Features

- **Ticket Endpoints**  
  - **List**: paginated, filterable by status/priority, searchable by title  
  - **Details**: ticket data + raw source JSON
- **Stats**: aggregated totals (open/closed, per-priority)  
- **Authentication**: JWT-based via DummyJSON `/auth/login`  
- **Caching**: Redis-backed TTL cache for tickets and stats  
- **Rate Limiting**: per‑IP request throttling with SlowAPI
- **Web Server**: Uvicorn ASGI web server implementation
- **Async**: HTTP calls with `httpx`, DB access with SQLAlchemy + SQLite/Postgres
- **Validation**: Pydantic models & auto‑generated OpenAPI docs
- **Testing**: unit and integration tests (pytest + httpx.MockTransport)
- **Dockerized**: `Dockerfile` + `docker-compose.yml`

---

## 🛠️ Tech Stack

| Layer         | Technology                       |
|---------------|----------------------------------|
| Language      | Python 3.11+                     |
| Web framework | FastAPI 0.111                    |
| HTTP client   | httpx 0.27                       |
| Web Server    | Uvicorn                          | 
| DB            | SQLAlchemy 2.x + SQLite/Postgres |
| Cache         | Redis (via `redis.asyncio`)      |
| Auth          | JWT (DummyJSON)                  |
| Rate Limit    | SlowAPI                          |
| Validation    | Pydantic 2.7                     |
| Testing       | pytest, httpx.MockTransport      |
| Container     | Docker, Docker Compose           |
| CI            | GitHub Actions, `ruff` linter    |

---

## 🔧 Environment Configuration

All runtime settings come from environment variables (12‑factor). Create:

- **`.env.local`** for development
- **`.env.test`** for tests
- **`.env`** for docker

Example `.env.local`:
```dotenv
APP_ENV=development
DATABASE_URL=sqlite+aiosqlite:///./tickets.db
REDIS_URL=redis://localhost:6379/0
EXTERNAL_API_URL=https://dummyjson.com
CACHE_TTL=300
LOG_LEVEL=INFO
RATE_LIMIT=100/minute
CACHING_ENABLED=1
```

Your Pydantic `Settings` class will auto‑load the correct file based on `APP_ENV`.

---

## 🔍 Setup & Local Development

1. **Clone**
   ```
    git clone git@github.com:Frans1905/Fran_Siric_tickethub.git
    cd tickethub
   ```
2. **Virtual env**
   ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
   ```
3. **Install**
   ```bash
    pip install -r requirements.txt
   ```
4. **Seed database** (once / after DB schema changes)
   ```bash
    make seed_db
   ```
5. **Run app locally**

    To run the app locally either a redis server needs to be set up, or CACHING_ENABLED needs to be set to 0 in .env.local.

   ```bash
    make run       # or
    PYTHONPATH=src uvicorn src.tickethub.main:app --reload
   ```

6. **Docs**
   - Swagger: http://127.0.0.1:8000/docs  
   - ReDoc:    http://127.0.0.1:8000/redoc

---

## 🧪 Testing

- **Unit tests** and **integration tests**:
  ```bash
    make test       #or
    PYTHONPATH=src APP_ENV=test pytest -v 
  ```

- **Test env** uses `.env.test` and a separate SQLite DB/Redis index

---

## Authentication through SwaggerUI


1. **Obtain a JWT**  
   - Navigate to Swagger UI: `http://127.0.0.1:8000/docs`  
   - Expand **`POST /auth/login`** and click **Try it out**  
   - Enter valid credentials (e.g. `username`: `emilys`, `password`: `emilyspass`)  
   - Execute to receive a JSON response including your `token`  

2. **Authorize in Swagger**  
   - Click the **Authorize** button (padlock icon) in the top‑right corner  
   - Paste the token
   - Click **Authorize** then **Close**

3. **Call protected endpoints**  
   - All routes with the **HTTPBearer** dependency will now include your JWT  
   - Explore `/tickets`, `/tickets/{id}`, `/tickets/stats`, etc.

> 👀 **Tip**: To discover other DummyJSON user credentials, view [https://dummyjson.com/users](https://dummyjson.com/users).

## 🐳 Docker & Docker Compose

```bash
make docker-build
make docker-up
```

- App: http://localhost:8000
- Redis: default port 6379

Compose uses `.env` in project root; refer to service hostnames (`redis`) for container connectivity.

---

## 📁 Project Structure

```
├── src/
│   └── tickethub/
│       ├── api/         # FastAPI routers
│       ├── services/    # Business logic + DB/cache/auth
│       ├── db/          # SQLAlchemy engine, session, seeder
│       ├── models/      # Pydantic & ORM models
│       ├── config.py    # Pydantic Settings
│       └── main.py      # FastAPI app setup
├── tests/               # pytest suites
├── docker/              # Dockerfile + compose
├── .env.local
├── .env.test
├── .env.production
├── Makefile
├── requirements.txt
└── README.md
```

---

## 🚀 CI/CD

GitHub Actions workflow at `.github/workflows/ci.yml` runs:
- `ruff` lint checks
- `pytest` tests
- `docker build`

---

## Usage of ChatGPT

ChatGPT was used to speed up the code development process and help with faster gathering of information. Was used for explaining of technologies, refactoring of code(with manual checks), 
help with debugging, etc...
