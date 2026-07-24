from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TeamFixtureSummary(BaseModel):
    team_id: int
    team_name: str
    average_difficulty_next_five: float
    next_five_opponents: str


class Fixture(BaseModel):
    fixture_id: int
    event_id: int | None
    event_name: str | None
    kickoff_time: datetime | None
    home_team_name: str
    home_team_short_name: str
    away_team_name: str
    away_team_short_name: str
    team_home_difficulty: int | None
    team_away_difficulty: int | None
    fixture_status: str
