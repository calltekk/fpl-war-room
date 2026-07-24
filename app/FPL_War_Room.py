from __future__ import annotations

from typing import Any, cast

import plotly.express as px
import streamlit as st

from app.components.player_card import render_player_card
from app.services.database import read_query
from app.styles.theme import apply_theme

st.set_page_config(
    page_title="FPL War Room",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

st.markdown(
    """
    <section class="war-header">
        <div class="war-kicker">Fantasy Premier League Intelligence</div>
        <div class="war-title">FPL War Room</div>
        <div class="war-subtitle">
            Fixture analysis, player discovery and eventually the machinery
            required to embarrass your brothers.
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

summary = read_query(
    """
    select
        count(*) as player_count,
        count(distinct team_name) as team_count,
        round(avg(current_price), 2) as average_player_price,
        round(avg(selected_by_percent), 2) as average_ownership
    from analytics_gold.player_shortlist
    """
)

fixture_summary = read_query(
    """
    select
        count(*) as fixture_count,
        count(*) filter (
            where fixture_status = 'upcoming'
        ) as upcoming_fixture_count,
        count(*) filter (
            where fixture_status = 'finished'
        ) as finished_fixture_count
    from analytics_silver.fct_fixtures
    """
)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

metric_col1.metric(
    "Available players",
    int(cast(int, summary.loc[0, "player_count"])),
)

metric_col2.metric(
    "Premier League teams",
    int(cast(int, summary.loc[0, "team_count"])),
)

metric_col3.metric(
    "Average price",
    f"£{cast(float, summary.loc[0, 'average_player_price']):.1f}m",
)

metric_col4.metric(
    "Fixtures loaded",
    int(cast(int, fixture_summary.loc[0, "fixture_count"])),
)

st.write("")

players = read_query(
    """
    select
        player_id,
        player_image_url,
        full_name,
        web_name,
        team_name,
        position_short_name,
        current_price,
        total_points,
        points_per_million,
        selected_by_percent,
        average_difficulty_next_five,
        ownership_category,
        fixture_outlook,
        next_five_opponents
    from analytics_gold.player_shortlist
    order by
        average_difficulty_next_five asc nulls last,
        selected_by_percent desc,
        current_price desc
    """
)

fixture_runs = read_query(
    """
    select
        team_name,
        average_difficulty_next_five,
        next_five_opponents
    from analytics_gold.team_fixture_summary
    order by
        average_difficulty_next_five asc,
        team_name
    """
)

overview_tab, players_tab, fixtures_tab = st.tabs(
    ["Command Centre", "Player Database", "Fixture Intelligence"]
)

with overview_tab:
    st.subheader("Pre-season watchlist")

    top_players = players.head(4)

    card_columns = st.columns(4)

    for column, (_, player) in zip(
        card_columns,
        top_players.iterrows(),
        strict=True,
    ):
        with column:
            render_player_card(cast(dict[str, Any], player.to_dict()))

    st.write("")
    st.subheader("Best fixture runs")

    chart = px.bar(
        fixture_runs,
        x="team_name",
        y="average_difficulty_next_five",
        hover_data=["next_five_opponents"],
        labels={
            "team_name": "Team",
            "average_difficulty_next_five": "Average FDR",
        },
    )

    chart.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f5f7fb",
        xaxis_tickangle=-45,
        margin={"l": 15, "r": 15, "t": 20, "b": 30},
    )

    st.plotly_chart(chart, use_container_width=True)

with players_tab:
    position_options = sorted(players["position_short_name"].dropna().unique().tolist())
    team_options = sorted(players["team_name"].dropna().unique().tolist())

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    selected_positions = filter_col1.multiselect(
        "Positions",
        options=position_options,
        default=position_options,
    )

    selected_teams = filter_col2.multiselect(
        "Teams",
        options=team_options,
    )

    maximum_price = filter_col3.slider(
        "Maximum price",
        min_value=float(players["current_price"].min()),
        max_value=float(players["current_price"].max()),
        value=float(players["current_price"].max()),
        step=0.1,
    )

    maximum_ownership = filter_col4.slider(
        "Maximum ownership",
        min_value=0.0,
        max_value=100.0,
        value=100.0,
        step=1.0,
    )

    filtered = players[
        players["position_short_name"].isin(selected_positions)
        & (players["current_price"] <= maximum_price)
        & (players["selected_by_percent"] <= maximum_ownership)
    ].copy()

    if selected_teams:
        filtered = filtered[filtered["team_name"].isin(selected_teams)]

    st.caption(f"{len(filtered)} players match the current filters.")

    st.dataframe(
        filtered[
            [
                "full_name",
                "team_name",
                "position_short_name",
                "current_price",
                "selected_by_percent",
                "average_difficulty_next_five",
                "fixture_outlook",
                "next_five_opponents",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "full_name": "Player",
            "team_name": "Club",
            "position_short_name": "Position",
            "current_price": st.column_config.NumberColumn(
                "Price",
                format="£%.1fm",
            ),
            "selected_by_percent": st.column_config.NumberColumn(
                "Ownership",
                format="%.1f%%",
            ),
            "average_difficulty_next_five": st.column_config.NumberColumn(
                "Next-five FDR",
                format="%.2f",
            ),
            "fixture_outlook": "Fixture outlook",
            "next_five_opponents": "Upcoming opponents",
        },
    )

with fixtures_tab:
    st.dataframe(
        fixture_runs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "team_name": "Club",
            "average_difficulty_next_five": st.column_config.NumberColumn(
                "Average FDR",
                format="%.2f",
            ),
            "next_five_opponents": "Next five",
        },
    )
