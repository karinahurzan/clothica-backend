# Clothica Backend

Clothica Backend is a FastAPI service that powers an online apparel store. It exposes RESTful endpoints for browsing products, managing user accounts, collecting feedback, and handling orders. The service relies on PostgreSQL for persistence and issues JWT tokens for authentication.

## Features
- FastAPI application with automatically generated OpenAPI docs.
- JWT-based authentication with refresh token support and logout token blacklisting.
- CRUD endpoints for goods, categories, orders, feedbacks, and newsletter subscriptions.
- SQLAlchemy ORM models backed by PostgreSQL.
- Seed script that imports sample categories, products, and feedback data.

## Tech Stack
- Python 3.11
- FastAPI & Starlette
- SQLAlchemy 2.x
- PostgreSQL 15
- Uvicorn ASGI server
- Docker & Docker Compose

## Local Development Setup

### 1. Prerequisites
- Docker Desktop (or Docker Engine + Docker Compose plugin)
- Optional: Python 3.11 + virtualenv (for running without Docker)

### 2. Environment Variables
Create an `.env` file in the project root with the application secrets and database URL:

```
SECRET_KEY=replace-with-strong-secret
ALGORITHM=HS256
DATABASE_URL=postgresql+psycopg2://postgres:pwdpwd@db:5432/clothica
```

For local execution outside Docker, update `DATABASE_URL` to point at your PostgreSQL instance (for example, `postgresql+psycopg2://postgres:pwdpwd@localhost:5432/clothica`).

### 3. Start the Stack (Docker)
1. Build and launch the containers:
	```bash
	docker compose up -d --build
	```
2. Apply seed data (optional but recommended for demo content):
	```bash
	docker compose exec web python seed.py
	```
3. API docs become available at http://localhost:8000/docs.

### 4. Run Without Docker (Optional)
1. Create and activate a virtual environment, then install dependencies:
	```bash
	python -m venv .venv
	.venv\Scripts\activate
	pip install --upgrade pip
	pip install -r requirements.txt
	```
2. Ensure PostgreSQL is running and the `DATABASE_URL` in `.env` points to it.
3. Initialize the schema and start the API server:
	```bash
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
	```
4. To load sample data, run `python seed.py` once the database is reachable.

## Project Structure
- [app/main.py](app/main.py) — FastAPI application factory and router registration.
- [app/models.py](app/models.py) — SQLAlchemy ORM models (users, goods, orders, etc.).
- [app/routers](app/routers) — Route handlers grouped by domain (auth, goods, orders…).
- [app/schemas.py](app/schemas.py) — Pydantic schemas used for request/response validation.
- [seed.py](seed.py) — Imports sample categories, goods, and feedback records.
- [docker-compose.yml](docker-compose.yml) and [Dockerfile](Dockerfile) — Containerized setup.

## Useful Commands
- Tail application logs: `docker compose logs -f web`
- Stop all services: `docker compose down`
- Run database migrations or maintenance tasks: `docker compose exec web bash`

## API Documentation
Interactive Swagger UI: http://localhost:8000/docs

The OpenAPI specification is exposed at http://localhost:8000/openapi.json for client generation or external tooling.