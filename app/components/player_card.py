from __future__ import annotations

from html import escape
from typing import Any

import streamlit as st

FALLBACK_IMAGE_URL = (
    "data:image/svg+xml;charset=UTF-8,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='110' height='140' "
    "viewBox='0 0 110 140'%3E"
    "%3Crect width='110' height='140' rx='12' fill='%2316283d'/%3E"
    "%3Ccircle cx='55' cy='43' r='24' fill='%239fb0c4'/%3E"
    "%3Cpath d='M18 132c2-34 17-52 37-52s35 18 37 52' "
    "fill='%239fb0c4'/%3E"
    "%3C/svg%3E"
)


def render_player_card(player: dict[str, Any]) -> None:
    name = escape(str(player.get("full_name") or "Unknown player"))
    team = escape(str(player.get("team_name") or "Unknown team"))
    position = escape(str(player.get("position_short_name") or "-"))
    price = float(player.get("current_price") or 0)
    ownership = float(player.get("selected_by_percent") or 0)

    difficulty = player.get("average_difficulty_next_five")
    difficulty_text = f"{float(difficulty):.2f}" if difficulty is not None else "N/A"

    card_html = f"""
<div class="player-card">
    <img
        class="player-image"
        src="{FALLBACK_IMAGE_URL}"
        alt="{name}"
    >
    <div class="player-name">{name}</div>
    <div class="player-meta">{team} · {position}</div>

    <div class="player-stats">
        <div class="player-stat">
            <div class="player-stat-label">Price</div>
            <div class="player-stat-value">£{price:.1f}m</div>
        </div>
        <div class="player-stat">
            <div class="player-stat-label">Owned</div>
            <div class="player-stat-value">{ownership:.1f}%</div>
        </div>
        <div class="player-stat">
            <div class="player-stat-label">Next 5</div>
            <div class="player-stat-value">{difficulty_text}</div>
        </div>
    </div>
</div>
"""

    st.html(card_html)
