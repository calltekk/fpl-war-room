from __future__ import annotations

from html import escape
from typing import Any

import streamlit as st


def render_player_card(
    player: dict[str, Any],
    rank: int,
) -> None:
    display_name = escape(
        str(player.get("web_name") or player.get("full_name") or "Unknown player")
    )
    team = escape(str(player.get("team_name") or "Unknown team"))
    position = escape(str(player.get("position_short_name") or "-"))
    price = float(player.get("current_price") or 0)
    expected_points = float(player.get("expected_points_next_5") or 0)
    difficulty = player.get("average_difficulty_next_5")
    opponents = escape(str(player.get("next_five_opponents") or "TBC"))

    difficulty_text = f"{float(difficulty):.2f}" if difficulty is not None else "TBC"

    initials = "".join(part[0].upper() for part in display_name.split() if part)[:2]

    st.html(
        f"""
<div class="target-card">
    <div class="target-card-top">
        <div class="target-rank">#{rank}</div>
        <div class="target-avatar">{initials}</div>
        <div class="target-identity">
            <div class="target-name">{display_name}</div>
            <div class="target-meta">{team} · {position}</div>
        </div>
    </div>

    <div class="target-metrics">
        <div class="target-metric">
            <span>5-GW xPts</span>
            <strong>{expected_points:.1f}</strong>
        </div>
        <div class="target-metric">
            <span>Price</span>
            <strong>£{price:.1f}m</strong>
        </div>
        <div class="target-metric">
            <span>Fixture run</span>
            <strong>{difficulty_text}</strong>
        </div>
    </div>

    <div class="target-fixtures">
        <span>Next five</span>
        <p>{opponents}</p>
    </div>
</div>
"""
    )
