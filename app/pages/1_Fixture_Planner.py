from __future__ import annotations

import streamlit as st

from app.services.database import read_query

st.set_page_config(
    page_title="Fixture Planner",
    page_icon="📅",
    layout="wide",
)

st.title("📅 Fixture Planner")

fixtures = read_query(
    """
    select
        event_id,
        event_name,
        kickoff_time,
        home_team_name,
        away_team_name,
        team_home_difficulty,
        team_away_difficulty,
        fixture_status
    from analytics_silver.fct_fixtures
    order by
        event_id,
        kickoff_time nulls last,
        fixture_id
    """
)

gameweeks = sorted(fixtures["event_id"].dropna().astype(int).unique().tolist())

selected_gameweeks = st.multiselect(
    "Gameweeks",
    options=gameweeks,
    default=gameweeks[:5],
)

filtered = fixtures[fixtures["event_id"].isin(selected_gameweeks)]

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "event_id": "GW",
        "event_name": "Gameweek",
        "kickoff_time": st.column_config.DatetimeColumn(
            "Kick-off",
            format="DD MMM YYYY, HH:mm",
        ),
        "home_team_name": "Home",
        "away_team_name": "Away",
        "team_home_difficulty": "Home FDR",
        "team_away_difficulty": "Away FDR",
        "fixture_status": "Status",
    },
)
