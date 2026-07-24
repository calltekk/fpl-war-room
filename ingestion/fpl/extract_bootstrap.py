from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from sqlalchemy import Engine, text

from ingestion.common.database import create_database_engine, database_connection
from ingestion.fpl.client import FPLClient


def save_raw_payload(payload: dict[str, Any]) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path("data/raw/fpl/bootstrap-static")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"bootstrap-static-{timestamp}.json"
    output_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    return output_path


def load_players(engine: Engine, players: list[dict[str, Any]]) -> int:
    statement = text(
        """
        INSERT INTO bronze.fpl_players (
            player_id,
            first_name,
            second_name,
            web_name,
            team_id,
            position_id,
            current_price,
            total_points,
            selected_by_percent,
            status,
            raw_payload,
            ingested_at
        )
        VALUES (
            :player_id,
            :first_name,
            :second_name,
            :web_name,
            :team_id,
            :position_id,
            :current_price,
            :total_points,
            :selected_by_percent,
            :status,
            CAST(:raw_payload AS JSONB),
            NOW()
        )
        ON CONFLICT (player_id)
        DO UPDATE SET
            first_name = EXCLUDED.first_name,
            second_name = EXCLUDED.second_name,
            web_name = EXCLUDED.web_name,
            team_id = EXCLUDED.team_id,
            position_id = EXCLUDED.position_id,
            current_price = EXCLUDED.current_price,
            total_points = EXCLUDED.total_points,
            selected_by_percent = EXCLUDED.selected_by_percent,
            status = EXCLUDED.status,
            raw_payload = EXCLUDED.raw_payload,
            ingested_at = NOW()
        """
    )

    records = [
        {
            "player_id": player["id"],
            "first_name": player["first_name"],
            "second_name": player["second_name"],
            "web_name": player["web_name"],
            "team_id": player["team"],
            "position_id": player["element_type"],
            "current_price": player["now_cost"] / 10,
            "total_points": player["total_points"],
            "selected_by_percent": player.get("selected_by_percent"),
            "status": player.get("status"),
            "raw_payload": json.dumps(player),
        }
        for player in players
    ]

    with database_connection(engine) as connection:
        connection.execute(statement, records)

    return len(records)


def load_teams(engine: Engine, teams: list[dict[str, Any]]) -> int:
    statement = text(
        """
        INSERT INTO bronze.fpl_teams (
            team_id,
            team_name,
            short_name,
            strength,
            raw_payload,
            ingested_at
        )
        VALUES (
            :team_id,
            :team_name,
            :short_name,
            :strength,
            CAST(:raw_payload AS JSONB),
            NOW()
        )
        ON CONFLICT (team_id)
        DO UPDATE SET
            team_name = EXCLUDED.team_name,
            short_name = EXCLUDED.short_name,
            strength = EXCLUDED.strength,
            raw_payload = EXCLUDED.raw_payload,
            ingested_at = NOW()
        """
    )

    records = [
        {
            "team_id": team["id"],
            "team_name": team["name"],
            "short_name": team["short_name"],
            "strength": team.get("strength"),
            "raw_payload": json.dumps(team),
        }
        for team in teams
    ]

    with database_connection(engine) as connection:
        connection.execute(statement, records)

    return len(records)


def load_events(engine: Engine, events: list[dict[str, Any]]) -> int:
    statement = text(
        """
        INSERT INTO bronze.fpl_events (
            event_id,
            event_name,
            deadline_time,
            is_current,
            is_next,
            is_previous,
            raw_payload,
            ingested_at
        )
        VALUES (
            :event_id,
            :event_name,
            :deadline_time,
            :is_current,
            :is_next,
            :is_previous,
            CAST(:raw_payload AS JSONB),
            NOW()
        )
        ON CONFLICT (event_id)
        DO UPDATE SET
            event_name = EXCLUDED.event_name,
            deadline_time = EXCLUDED.deadline_time,
            is_current = EXCLUDED.is_current,
            is_next = EXCLUDED.is_next,
            is_previous = EXCLUDED.is_previous,
            raw_payload = EXCLUDED.raw_payload,
            ingested_at = NOW()
        """
    )

    records = [
        {
            "event_id": event["id"],
            "event_name": event["name"],
            "deadline_time": event.get("deadline_time"),
            "is_current": event.get("is_current", False),
            "is_next": event.get("is_next", False),
            "is_previous": event.get("is_previous", False),
            "raw_payload": json.dumps(event),
        }
        for event in events
    ]

    with database_connection(engine) as connection:
        connection.execute(statement, records)

    return len(records)


def run() -> None:
    pipeline_run_id = uuid4()
    started_at = datetime.now(UTC)
    engine = create_database_engine()

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
                "pipeline_name": "fpl_bootstrap_static",
                "started_at": started_at,
                "status": "RUNNING",
            },
        )

    try:
        with FPLClient() as client:
            payload = client.get_bootstrap_static()

        raw_path = save_raw_payload(payload)
        player_count = load_players(engine, payload["elements"])
        team_count = load_teams(engine, payload["teams"])
        event_count = load_events(engine, payload["events"])

        total_records = player_count + team_count + event_count

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
                    "records_extracted": total_records,
                    "records_loaded": total_records,
                    "pipeline_run_id": pipeline_run_id,
                },
            )

        print(f"Raw payload saved to: {raw_path}")
        print(f"Players loaded: {player_count}")
        print(f"Teams loaded: {team_count}")
        print(f"Events loaded: {event_count}")

    except Exception as exc:
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
                    "error_message": str(exc),
                    "pipeline_run_id": pipeline_run_id,
                },
            )

        raise


if __name__ == "__main__":
    run()
