from __future__ import annotations

from fastapi import APIRouter, Query

from api.schemas.player import (
    CaptainProjection,
    DifferentialProjection,
    PlayerProjection,
)
from api.services.database import fetch_all

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/projections", response_model=list[PlayerProjection])
def get_player_projections(
    limit: int = Query(default=50, ge=1, le=200),
) -> list[PlayerProjection]:
    rows = fetch_all(
        f"""
        select
            player_id,
            player_code,
            photo_filename,
            player_image_url,
            web_name,
            team_name,
            team_short_name,
            team_code,
            badge_url,
            position_short_name,
            current_price::float as current_price,
            selected_by_percent::float as selected_by_percent,
            expected_points_next_3::float as expected_points_next_3,
            expected_points_next_5::float as expected_points_next_5,
            expected_points_per_million::float
                as expected_points_per_million,
            average_difficulty_next_5::float
                as average_difficulty_next_5,
            next_five_opponents,
            expected_points_rank_overall
        from analytics_gold.player_expected_points_summary
        order by expected_points_rank_overall
        limit {limit}
        """
    )

    return [PlayerProjection(**dict(row)) for row in rows]


@router.get("/captains", response_model=list[CaptainProjection])
def get_captain_projections(
    limit: int = Query(default=10, ge=1, le=50),
) -> list[CaptainProjection]:
    rows = fetch_all(
        f"""
        select
            captain_rank,
            web_name,
            team_name,
            team_short_name,
            team_code,
            badge_url,
            expected_points_next_3::float as expected_points_next_3,
            captain_points_next_3::float as captain_points_next_3,
            next_five_opponents
        from analytics_gold.captain_rankings
        order by captain_rank
        limit {limit}
        """
    )

    return [CaptainProjection(**dict(row)) for row in rows]


@router.get(
    "/differentials",
    response_model=list[DifferentialProjection],
)
def get_differentials(
    limit: int = Query(default=20, ge=1, le=100),
) -> list[DifferentialProjection]:
    rows = fetch_all(
        f"""
        select
            differential_rank,
            web_name,
            team_name,
            team_short_name,
            team_code,
            badge_url,
            position_short_name,
            current_price::float as current_price,
            selected_by_percent::float as selected_by_percent,
            expected_points_next_5::float as expected_points_next_5,
            differential_score::float as differential_score,
            next_five_opponents
        from analytics_gold.differential_targets
        order by differential_rank
        limit {limit}
        """
    )

    return [DifferentialProjection(**dict(row)) for row in rows]
