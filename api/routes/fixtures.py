from __future__ import annotations

from fastapi import APIRouter, Query

from api.schemas.fixture import Fixture, TeamFixtureSummary
from api.services.database import fetch_all

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


@router.get("/team-summary", response_model=list[TeamFixtureSummary])
def get_team_fixture_summary() -> list[TeamFixtureSummary]:
    rows = fetch_all(
        """
        select
            team_id,
            team_name,
            team_short_name,
            team_code,
            badge_url,
            average_difficulty_next_five::float
                as average_difficulty_next_five,
            next_five_opponents
        from analytics_gold.team_fixture_summary
        order by average_difficulty_next_five, team_name
        """
    )

    return [TeamFixtureSummary(**dict(row)) for row in rows]


@router.get("", response_model=list[Fixture])
def get_fixtures(
    gameweek: int | None = Query(default=None, ge=1, le=38),
) -> list[Fixture]:
    where_clause = ""

    if gameweek is not None:
        where_clause = f"where event_id = {gameweek}"

    rows = fetch_all(
        f"""
        select
            fixture_id,
            event_id,
            event_name,
            kickoff_time,
            home_team_name,
            home_team_short_name,
            away_team_name,
            away_team_short_name,
            team_home_difficulty,
            team_away_difficulty,
            fixture_status
        from analytics_silver.fct_fixtures
        {where_clause}
        order by event_id, kickoff_time nulls last, fixture_id
        """
    )

    return [Fixture(**dict(row)) for row in rows]
