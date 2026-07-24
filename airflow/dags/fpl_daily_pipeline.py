from __future__ import annotations

import subprocess
from datetime import datetime, timedelta

from airflow.sdk import DAG, task


PROJECT_ROOT = "/opt/fpl-war-room"
DBT_ROOT = f"{PROJECT_ROOT}/dbt/fpl_analytics"
DBT_PROFILES = f"{PROJECT_ROOT}/dbt/profiles"


def run_command(command: list[str], cwd: str = PROJECT_ROOT) -> None:
    subprocess.run(
        command,
        cwd=cwd,
        check=True,
    )


with DAG(
    dag_id="fpl_daily_pipeline",
    description="Ingest FPL data, rebuild dbt models, and run validation checks.",
    start_date=datetime(2026, 7, 24),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["fpl", "dbt", "portfolio"],
) as dag:

    @task
    def ingest_bootstrap() -> None:
        run_command(
            [
                "python",
                "-m",
                "ingestion.fpl.extract_bootstrap",
            ]
        )

    @task
    def ingest_fixtures() -> None:
        run_command(
            [
                "python",
                "-m",
                "ingestion.fpl.extract_fixtures",
            ]
        )

    @task
    def dbt_build() -> None:
        run_command(
            [
                "dbt",
                "build",
                "--profiles-dir",
                DBT_PROFILES,
            ],
            cwd=DBT_ROOT,
        )

    @task
    def validate_gold_data() -> None:
        run_command(
            [
                "python",
                "-c",
                (
                    "from api.services.database import fetch_one; "
                    "row = fetch_one("
                    "\"select count(*) as row_count "
                    "from analytics_gold.player_expected_points_summary\""
                    "); "
                    "assert row is not None; "
                    "assert row['row_count'] > 0; "
                    "print(f\"Validated {row['row_count']} gold player rows\")"
                ),
            ]
        )

    bootstrap = ingest_bootstrap()
    fixtures = ingest_fixtures()

    bootstrap >> fixtures >> dbt_build() >> validate_gold_data()
