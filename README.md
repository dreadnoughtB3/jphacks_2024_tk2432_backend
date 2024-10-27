## 手順
1. docker compose build
2. docker compose run --entrypoint "poetry install --no-root" backend
3. docker compose up

## migration
1. docker compose exec backend poetry run alembic revision --autogenerate
2. Fix versions file (import sqlmodel)
3. docker compose exec backend poetry run alembic upgrade head