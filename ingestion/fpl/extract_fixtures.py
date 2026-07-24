from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Engine, text

from ingestion.common.database import create_database_engine, database_connection
from ingestion.fpl.client import FPLClient

PIPELINE_NAME = "fpl_fixtures"


def save_raw_payload(fixtures: list[dict[str, Any]]) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path("data/raw/fpl/fixtures")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"fixtures-{timestamp}.json"
    output_path.write_text(
        json.dumps(fixtures, indent=2),
        encoding="utf-8",
    )

    return output_path


def start_pipeline_run(engine: Engine) -> UUID:
    pipeline_run_id = uuid4()

    with database_connection(engine) as connection:
        connection.execute(
            text(
                """
                INSERT INTO audit.pipeline_runs (
                    pipeline_run_id,
                    pipeline_name,
                    started_at,
                    status
                )
                VALUES (
                    :pipeline_run_id,
                    :pipeline_name,
                    :started_at,
                    :status
                )
                """
            ),
            {
                "pipeline_run_id": pipeline_run_id,
                "pipeline_name": PIPELINE_NAME,
                "started_at": datetime.now(UTC),
                "status": "RUNNING",
            },
        )

    return pipeline_run_id


def mark_pipeline_success(
    engine: Engine,
    pipeline_run_id: UUID,
    record_count: int,
) -> None:
    with database_connection(engine) as connection:
        connection.execute(
            text(
                """
                UPDATE audit.pipeline_runs
                SET
                    completed_at = :completed_at,
                    status = :status,
                    records_extracted = :records_extracted,
                    records_loaded = :records_loaded
                WHERE pipeline_run_id = :pipeline_run_id
                """
            ),
            {
                "completed_at": datetime.now(UTC),
                "status": "SUCCESS",
                "records_extracted": record_count,
                "records_loaded": record_count,
                "pipeline_run_id": pipeline_run_id,
            },
        )


def mark_pipeline_failed(
    engine: Engine,
    pipeline_run_id: UUID,
    error_message: str,
) -> None:
    with database_connection(engine) as connection:
        connection.execute(
            text(
                """
                UPDATE audit.pipeline_runs
                SET
                    completed_at = :completed_at,
                    status = :status,
                    error_message = :error_message
                WHERE pipeline_run_id = :pipeline_run_id
                """
            ),
            {
                "completed_at": datetime.now(UTC),
                "status": "FAILED",
                "error_message": error_message,
                "pipeline_run_id": pipeline_run_id,
            },
        )


def load_fixtures(
    engine: Engine,
    fixtures: list[dict[str, Any]],
) -> int:
    statement = text(
        """
        INSERT INTO bronze.fpl_fixtures (
            fixture_id,
            event_id,
            kickoff_time,
            team_home_id,
            team_away_id,
            team_home_score,
            team_away_score,
            team_home_difficulty,
            team_away_difficulty,
            finished,
            started,
            provisional_start_time,
            minutes,
            raw_payload,
            ingested_at
        )
        VALUES (
            :fixture_id,
            :event_id,
            :kickoff_time,
            :team_home_id,
            :team_away_id,
            :team_home_score,
            :team_away_score,
            :team_home_difficulty,
            :team_away_difficulty,
            :finished,
            :started,
            :provisional_start_time,
            :minutes,
            CAST(:raw_payload AS JSONB),
            NOW()
        )
        ON CONFLICT (fixture_id)
        DO UPDATE SET
            event_id = EXCLUDED.event_id,
            kickoff_time = EXCLUDED.kickoff_time,
            team_home_id = EXCLUDED.team_home_id,
            team_away_id = EXCLUDED.team_away_id,
            team_home_score = EXCLUDED.team_home_score,
            team_away_score = EXCLUDED.team_away_score,
            team_home_difficulty = EXCLUDED.team_home_difficulty,
            team_away_difficulty = EXCLUDED.team_away_difficulty,
            finished = EXCLUDED.finished,
            started = EXCLUDED.started,
            provisional_start_time = EXCLUDED.provisional_start_time,
            minutes = EXCLUDED.minutes,
            raw_payload = EXCLUDED.raw_payload,
            ingested_at = NOW()
        """
    )

    records = [
        {
            "fixture_id": fixture["id"],
            "event_id": fixture.get("event"),
            "kickoff_time": fixture.get("kickoff_time"),
            "team_home_id": fixture["team_h"],
            "team_away_id": fixture["team_a"],
            "team_home_score": fixture.get("team_h_score"),
            "team_away_score": fixture.get("team_a_score"),
            "team_home_difficulty": fixture.get("team_h_difficulty"),
            "team_away_difficulty": fixture.get("team_a_difficulty"),
            "finished": fixture.get("finished", False),
            "started": fixture.get("started", False),
            "provisional_start_time": fixture.get(
                "provisional_start_time",
                False,
            ),
            "minutes": fixture.get("minutes", 0),
            "raw_payload": json.dumps(fixture),
        }
        for fixture in fixtures
    ]

    if not records:
        return 0

    with database_connection(engine) as connection:
        connection.execute(statement, records)

    return len(records)


def run() -> None:
    engine = create_database_engine()
    pipeline_run_id = start_pipeline_run(engine)

    try:
        with FPLClient() as client:
            fixtures = client.get_fixtures()

        raw_path = save_raw_payload(fixtures)
        fixture_count = load_fixtures(engine, fixtures)

        mark_pipeline_success(
            engine=engine,
            pipeline_run_id=pipeline_run_id,
            record_count=fixture_count,
        )

        print(f"Raw payload saved to: {raw_path}")
        print(f"Fixtures loaded: {fixture_count}")

    except Exception as exc:
        mark_pipeline_failed(
            engine=engine,
            pipeline_run_id=pipeline_run_id,
            error_message=str(exc),
        )
        raise


if __name__ == "__main__":
    run()
