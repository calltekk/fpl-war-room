from __future__ import annotations

from pydantic import BaseModel


class PlayerProjection(BaseModel):
    player_id: int
    player_code: int | None
    photo_filename: str | None
    player_image_url: str | None
    web_name: str
    team_name: str
    team_short_name: str
    team_code: int | None
    badge_url: str | None
    position_short_name: str
    current_price: float
    selected_by_percent: float
    expected_points_next_3: float
    expected_points_next_5: float
    expected_points_per_million: float
    average_difficulty_next_5: float
    next_five_opponents: str
    expected_points_rank_overall: int


class CaptainProjection(BaseModel):
    captain_rank: int
    web_name: str
    team_name: str
    team_short_name: str
    team_code: int | None
    badge_url: str | None
    expected_points_next_3: float
    captain_points_next_3: float
    next_five_opponents: str


class DifferentialProjection(BaseModel):
    differential_rank: int
    web_name: str
    team_name: str
    team_short_name: str
    team_code: int | None
    badge_url: str | None
    position_short_name: str
    current_price: float
    selected_by_percent: float
    expected_points_next_5: float
    differential_score: float
    next_five_opponents: str
