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
        full_name,
        web_name,
        team_name,
        position_short_name,
        current_price,
        selected_by_percent,
        expected_points_next_3,
        expected_points_next_5,
        expected_points_per_million,
        average_difficulty_next_5,
        expected_points_rank_overall,
        expected_points_rank_by_position,
        next_five_opponents
    from analytics_gold.player_expected_points_summary
    order by expected_points_rank_overall
    """
)

captains = read_query(
    """
    select
        captain_rank,
        web_name as full_name,
        team_name,
        expected_points_next_3,
        captain_points_next_3,
        next_five_opponents
    from analytics_gold.captain_rankings
    order by captain_rank
    limit 5
    """
)

differentials = read_query(
    """
    select
        differential_rank,
        web_name as full_name,
        team_name,
        position_short_name,
        current_price,
        selected_by_percent,
        expected_points_next_5,
        differential_score,
        next_five_opponents
    from analytics_gold.differential_targets
    order by differential_rank
    limit 10
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
    st.subheader("Top projected targets")
    st.caption("Baseline projections over each player's next five fixtures.")

    top_players = players.head(4)

    card_columns = st.columns(4)

    for rank, (column, (_, player)) in enumerate(
        zip(
            card_columns,
            top_players.iterrows(),
            strict=True,
        ),
        start=1,
    ):
        with column:
            render_player_card(
                cast(dict[str, Any], player.to_dict()),
                rank=rank,
            )

    st.write("")

    recommendation_col1, recommendation_col2 = st.columns(2)

    with recommendation_col1:
        st.subheader("Captain picks")
        st.caption("Highest projected returns across the next three fixtures.")

        captain_display = captains.rename(
            columns={
                "captain_rank": "Rank",
                "full_name": "Player",
                "team_name": "Club",
                "expected_points_next_3": "3-GW xPts",
                "captain_points_next_3": "Captain xPts",
                "next_five_opponents": "Fixtures",
            }
        )

        st.dataframe(
            captain_display[
                [
                    "Rank",
                    "Player",
                    "Club",
                    "3-GW xPts",
                    "Captain xPts",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            height=245,
            column_config={
                "3-GW xPts": st.column_config.NumberColumn(format="%.1f"),
                "Captain xPts": st.column_config.NumberColumn(format="%.1f"),
            },
        )

    with recommendation_col2:
        st.subheader("Differential targets")
        st.caption("Low-owned players with strong projected upside.")

        differential_display = differentials.rename(
            columns={
                "differential_rank": "Rank",
                "full_name": "Player",
                "team_name": "Club",
                "position_short_name": "Pos",
                "current_price": "Price",
                "selected_by_percent": "Owned",
                "expected_points_next_5": "5-GW xPts",
                "differential_score": "Score",
            }
        )

        st.dataframe(
            differential_display[
                [
                    "Rank",
                    "Player",
                    "Club",
                    "Pos",
                    "Price",
                    "Owned",
                    "5-GW xPts",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            height=245,
            column_config={
                "Price": st.column_config.NumberColumn(format="£%.1fm"),
                "Owned": st.column_config.NumberColumn(format="%.1f%%"),
                "5-GW xPts": st.column_config.NumberColumn(format="%.1f"),
            },
        )

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
                "average_difficulty_next_5",
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
            "average_difficulty_next_5": st.column_config.NumberColumn(
                "Next-five FDR",
                format="%.2f",
            ),
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
            "average_difficulty_next_5": st.column_config.NumberColumn(
                "Average FDR",
                format="%.2f",
            ),
            "next_five_opponents": "Next five",
        },
    )
