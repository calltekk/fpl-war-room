# FPL War Room

A full-stack Fantasy Premier League decision platform built as an end-to-end data engineering portfolio project.

FPL War Room ingests live Fantasy Premier League data, stores it in a layered PostgreSQL warehouse, transforms it with dbt, serves analytical outputs through FastAPI, and presents them in a responsive Next.js dashboard.

**Live application:** https://fpl-war-room-lac.vercel.app  
**API documentation:** https://fpl-war-room-api.onrender.com/docs  
**API health check:** https://fpl-war-room-api.onrender.com/health

> The deployed Command Centre is currently the primary working dashboard. Additional planning and analysis modules are on the roadmap.

---

## What the project demonstrates

- Production-style Bronze, Silver and Gold data modelling
- Automated ingestion from a public REST API
- SQL transformations and data-quality testing with dbt
- Workflow orchestration with Apache Airflow
- A typed FastAPI analytics service
- A responsive Next.js and TypeScript frontend
- Hosted PostgreSQL with encrypted connections
- Continuous integration through Azure DevOps
- Cloud deployment across Neon, Render and Vercel
- Containerised local development with Docker Compose

---

## Architecture

```text
Fantasy Premier League API
            |
            v
Python ingestion pipelines
            |
            v
PostgreSQL / Neon
  Bronze -> Silver -> Gold
            |
            v
           dbt
            |
            v
        FastAPI API
            |
            v
 Next.js Command Centre
```

Airflow orchestrates the local end-to-end pipeline:

```text
ingest_bootstrap
        |
ingest_fixtures
        |
    dbt_build
        |
validate_gold_data
```

---

## Technology stack

| Layer | Technology |
|---|---|
| Data source | Fantasy Premier League API |
| Ingestion | Python, HTTPX, Pandas |
| Database | PostgreSQL 17, Neon |
| Transformations | dbt-postgres |
| Orchestration | Apache Airflow 3 |
| Backend | FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS, shadcn/ui |
| Containers | Docker, Docker Compose |
| CI | Azure DevOps Pipelines |
| Hosting | Vercel, Render, Neon |
| Testing and quality | pytest, Ruff, mypy, dbt tests, ESLint |

---

## Data platform

### Bronze

Raw FPL entities are ingested into PostgreSQL while the original API responses are also retained as timestamped JSON files.

Current Bronze datasets include:

- players
- teams
- gameweeks
- fixtures

### Silver

The Silver layer cleans, types and enriches the raw FPL data into reusable analytical entities, including standardised player and fixture models.

### Gold

The Gold layer contains decision-ready datasets consumed by the API and frontend, including:

- player expected-points summaries
- captaincy rankings
- differential-player rankings
- team fixture summaries

The present expected-points logic is a transparent analytical baseline. A future version will introduce backtested fixture and player models based on historical results, team strength, home advantage, form and squad changes.

---

## Current application

The deployed Command Centre provides a consolidated view of:

- leading player projections
- captaincy candidates
- differential options
- upcoming fixture summaries
- data-refresh status

Planned modules include:

- My Squad analysis
- Transfer Planner
- dedicated Captaincy analysis
- advanced Fixtures view
- mini-league rival analysis
- machine-learning fixture predictions

---

## API endpoints

Interactive OpenAPI documentation is available at:

```text
https://fpl-war-room-api.onrender.com/docs
```

Key endpoints include:

```text
GET /health
GET /players/projections
GET /players/captains
GET /players/differentials
GET /fixtures/team-summary
GET /status/data-refresh
```

---

## Repository structure

```text
fpl-war-room/
├── airflow/                    # Airflow DAGs and orchestration code
├── api/                        # FastAPI application
├── data/raw/                   # Timestamped raw FPL payloads
├── dbt/
│   ├── fpl_analytics/          # dbt project and models
│   └── profiles/               # environment-driven dbt profile
├── frontend/                   # Next.js application
├── infrastructure/            # PostgreSQL initialisation and infrastructure files
├── ingestion/                 # Python extraction and loading pipelines
├── tests/                      # Python tests
├── azure-pipelines.yml         # Azure DevOps CI pipeline
├── docker-compose.yml          # Local PostgreSQL and supporting services
├── docker-compose.airflow.yml  # Local Airflow stack
└── pyproject.toml              # Python project and tooling configuration
```

---

## Running locally

### Prerequisites

- Python 3.12
- Node.js 20 or later
- Docker and Docker Compose
- PostgreSQL client tools are useful for inspection

### 1. Clone the repository

```bash
git clone https://github.com/calltekk/fpl-war-room.git
cd fpl-war-room
```

### 2. Create the Python environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Configure database variables

Create a local environment file from your own PostgreSQL credentials:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fpl
POSTGRES_USER=fpl_user
POSTGRES_PASSWORD=your_password
POSTGRES_SSLMODE=prefer
```

Never commit credentials or hosted database connection strings.

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Run ingestion

```bash
python -m ingestion.fpl.extract_bootstrap
python -m ingestion.fpl.extract_fixtures
```

### 6. Build the dbt project

```bash
cd dbt/fpl_analytics
../../.venv/bin/dbt build --profiles-dir ../profiles
cd ../..
```

### 7. Start the API

```bash
PYTHONPATH=. uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### 8. Start the frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

The dashboard will be available at `http://localhost:3000`.

---

## Airflow orchestration

Start the Airflow stack with:

```bash
docker compose -f docker-compose.airflow.yml up -d
```

The DAG executes ingestion, dbt transformations and Gold-layer validation as a single dependency-controlled workflow.

---

## Continuous integration

The Azure DevOps pipeline validates the project on every change to `main`.

It includes:

- Ruff linting
- mypy type checking
- pytest tests
- temporary PostgreSQL service provisioning
- live FPL ingestion
- dbt build and tests
- Gold-layer validation
- frontend lint and production build
- Docker Compose configuration validation

This ensures application code, transformations and infrastructure configuration are tested together rather than as isolated components.

---

## Deployment

| Component | Platform |
|---|---|
| Frontend | Vercel |
| FastAPI service | Render |
| PostgreSQL warehouse | Neon |
| CI pipeline | Azure DevOps |
| Local orchestration | Apache Airflow |

The Render service uses the free tier and may require a brief cold start after inactivity.

---

## Roadmap

The next major phase is an evidence-based fixture model that improves on generic one-to-five difficulty ratings.

Proposed outputs include:

- expected goals scored and conceded
- clean-sheet probability
- win, draw and loss probabilities
- separate attacking and defensive fixture difficulty
- prediction confidence
- time-based model backtesting
- model monitoring and versioned prediction tables

The first version will compare a transparent statistical baseline against Poisson and gradient-boosting models before any model is promoted into the application.

---

## Project status

This project is actively under development. The deployed Command Centre and its supporting data platform are operational; additional product modules and predictive modelling are planned.

---

## Author

Built by **Callum Hilton** as a practical demonstration of modern data engineering, analytics engineering and full-stack delivery applied to football data.
