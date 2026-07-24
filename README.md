# FPL War Room

A full-stack Fantasy Premier League analytics platform built as an end-to-end data engineering portfolio project.

**Live app:** https://fpl-war-room-lac.vercel.app  
**API docs:** https://fpl-war-room-api.onrender.com/docs

## Overview

FPL War Room ingests live Fantasy Premier League data, stores it in a PostgreSQL warehouse, transforms it through Bronze, Silver and Gold layers with dbt, serves analytical outputs through FastAPI, and displays them in a Next.js dashboard.

The current Command Centre includes:

- player projections
- captaincy rankings
- differential picks
- fixture summaries
- pipeline refresh status

## Architecture

```text
FPL API
  ↓
Python ingestion
  ↓
PostgreSQL / Neon
Bronze → Silver → Gold
  ↓
dbt
  ↓
FastAPI
  ↓
Next.js dashboard
```

Apache Airflow orchestrates ingestion, dbt builds and Gold-layer validation locally.

## Tech stack

- Python, HTTPX, Pandas
- PostgreSQL 17 and Neon
- dbt-postgres
- Apache Airflow 3
- FastAPI, SQLAlchemy and Pydantic
- Next.js, React, TypeScript and Tailwind CSS
- Docker Compose
- Azure DevOps CI
- Vercel and Render

## Data model

- **Bronze:** raw players, teams, gameweeks and fixtures
- **Silver:** cleaned and standardised player and fixture models
- **Gold:** expected points, captains, differentials and team fixture summaries

## Local development

```bash
git clone https://github.com/calltekk/fpl-war-room.git
cd fpl-war-room

python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .

docker compose up -d

python -m ingestion.fpl.extract_bootstrap
python -m ingestion.fpl.extract_fixtures

cd dbt/fpl_analytics
../../.venv/bin/dbt build --profiles-dir ../profiles
```

Start the API:

```bash
PYTHONPATH=. uvicorn api.main:app --reload --port 8000
```

Start the frontend:

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## CI/CD

The Azure DevOps pipeline runs:

- Ruff, mypy and pytest
- PostgreSQL integration tests
- live FPL ingestion
- dbt build and tests
- Gold-layer validation
- frontend lint and build
- Docker Compose validation

## Roadmap

- My Squad analysis
- Transfer Planner
- dedicated Fixtures and Captaincy pages
- mini-league rival analysis
- backtested machine-learning fixture predictions

Built by **Callum Hilton**.
