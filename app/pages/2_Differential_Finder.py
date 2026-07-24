from __future__ import annotations

import plotly.express as px
import streamlit as st

from app.services.database import read_query

st.set_page_config(
    page_title="Differential Finder",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Differential Finder")

players = read_query(
    """
    select
        full_name,
        team_name,
        position_short_name,
        current_price,
        selected_by_percent,
        points_per_million,
        average_difficulty_next_five,
        fixture_outlook,
        next_five_opponents
    from analytics_gold.player_shortlist
    where selected_by_percent < 10
    order by
        average_difficulty_next_five asc nulls last,
        points_per_million desc
    """
)

ownership_limit = st.slider(
    "Maximum ownership",
    min_value=1.0,
    max_value=15.0,
    value=5.0,
    step=0.5,
)

price_limit = st.slider(
    "Maximum price",
    min_value=float(players["current_price"].min()),
    max_value=float(players["current_price"].max()),
    value=float(players["current_price"].max()),
    step=0.1,
)

filtered = players[
    (players["selected_by_percent"] <= ownership_limit) & (players["current_price"] <= price_limit)
].copy()

st.metric(
    "Matching differentials",
    len(filtered),
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)

if not filtered.empty:
    chart = px.scatter(
        filtered,
        x="average_difficulty_next_five",
        y="current_price",
        size="selected_by_percent",
        hover_name="full_name",
        hover_data=[
            "team_name",
            "position_short_name",
            "next_five_opponents",
        ],
        labels={
            "average_difficulty_next_five": "Average fixture difficulty",
            "current_price": "Price (£m)",
            "selected_by_percent": "Ownership (%)",
        },
        title="Low-owned players by price and fixture run",
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
    )
else:
    st.info("No players match the current filters.")
