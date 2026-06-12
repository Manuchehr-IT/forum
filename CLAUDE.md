# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the application:**
```bash
# Full stack via Docker
docker-compose up

# Backend only (local)
cd backend && python3 -m src.main
```

**Database migrations:**
```bash
cd backend
alembic upgrade head          # apply migrations
alembic revision --autogenerate -m "description"  # create migration
```

**Seed the database:**
```bash
cd backend && python3 src/scripts/seed_db.py
```

**Environment setup:** Copy `.env.example` → `.env` and `backend/.env.example` → `backend/.env`, then fill in values.

## Architecture

This is a **FastAPI forum backend** following Clean Architecture / DDD with four strict layers:

```
domain/       → Entities, value objects, aggregates, domain interfaces (no dependencies on outer layers)
application/  → Use cases (commands/queries), orchestrates domain logic
infrastructure/ → DB repositories, ORM models, external services (OpenAI, Telegram, Redis, file storage)
api/          → FastAPI routers, request/response schemas, HTTP exception handlers
```

**Request flow:** `api/v1/<resource>/router.py` → `application/<resource>/use_cases.py` → `domain/<resource>/` entities, persisted via `infrastructure/database/repositories/`

### Key structural patterns

- **Unit of Work** (`infrastructure/database/uow.py`): wraps repository commits in a single transaction; use cases receive a UoW instance, not raw session.
- **Mappers** (`infrastructure/database/mappers/`): bidirectional conversion between SQLAlchemy ORM models and domain entities; never expose ORM models above the infrastructure layer.
- **Dependency injection** (`api/dependencies.py`): FastAPI `Depends()` wires repositories, UoW, services, and auth into use cases.
- **Domain interfaces** (`domain/interfaces/`): abstract base classes for storage, LLM, and validation; infrastructure provides concrete implementations.

### Domain model highlights

- **Forum hierarchy:** `Section` → `Theme` → `Message`
- **Polymorphic messages:** `Post`, `Task`, `Comment`, `TaskAssignment` share a base `Message` aggregate root; discriminated in the ORM via a type column.
- **Auth:** Telegram OAuth issues a JWT; `infrastructure/auth/` handles both token creation and Telegram callback verification.
- **AI integration:** `infrastructure/services/openai/` wraps the OpenAI API; `application/llm/` contains the use cases that call it.
- **Media files:** uploaded files are validated (`infrastructure/services/validation/`), stored locally (`infrastructure/services/storage/`), and attached to messages via `application/messages/media_attachment_service.py`.

### Configuration

All settings are Pydantic `BaseSettings` models in `backend/src/core/config/settings.py`, loaded from environment variables. Notable groups: `AppSettings`, `DatabaseSettings`, `RedisSettings`, `JWTSettings`, `OpenAISettings`, `TelegramSettings`, `StorageSettings`.

### Services (Docker Compose)

| Service    | Port |
|------------|------|
| Backend    | 8000 |
| PostgreSQL | 5432 |
| Redis      | 6379 |
