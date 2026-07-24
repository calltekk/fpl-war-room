from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --war-bg: #07121f;
            --war-panel: #101f31;
            --war-panel-soft: #16283d;
            --war-text: #f5f7fb;
            --war-muted: #9fb0c4;
            --war-green: #00ff87;
            --war-purple: #8b5cf6;
            --war-pink: #e90052;
            --war-border: rgba(255, 255, 255, 0.08);
        }

        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(139, 92, 246, 0.16),
                    transparent 35%
                ),
                var(--war-bg);
            color: var(--war-text);
        }

        [data-testid="stSidebar"] {
            background: #091827;
            border-right: 1px solid var(--war-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--war-text);
        }

        [data-testid="stHeader"] {
            background: rgba(7, 18, 31, 0.75);
        }

        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: var(--war-text);
            letter-spacing: -0.02em;
        }

        .war-header {
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.4rem;
            border: 1px solid var(--war-border);
            border-radius: 22px;
            background:
                linear-gradient(
                    120deg,
                    rgba(139, 92, 246, 0.28),
                    rgba(0, 255, 135, 0.08)
                ),
                var(--war-panel);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
        }

        .war-kicker {
            color: var(--war-green);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .war-title {
            color: var(--war-text);
            font-size: 2.4rem;
            font-weight: 850;
            line-height: 1;
            margin-bottom: 0.6rem;
        }

        .war-subtitle {
            color: var(--war-muted);
            font-size: 1rem;
        }

        [data-testid="stMetric"] {
            background: var(--war-panel);
            border: 1px solid var(--war-border);
            border-radius: 18px;
            padding: 1rem 1.15rem;
            min-height: 112px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.16);
        }

        [data-testid="stMetricLabel"] {
            color: var(--war-muted);
        }

        [data-testid="stMetricValue"] {
            color: var(--war-green);
        }

        .player-card {
            position: relative;
            overflow: hidden;
            min-height: 242px;
            border-radius: 20px;
            border: 1px solid var(--war-border);
            background:
                linear-gradient(
                    155deg,
                    rgba(139, 92, 246, 0.2),
                    rgba(16, 31, 49, 0.96) 48%
                );
            padding: 1.1rem;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2);
        }

        .player-image {
            display: block;
            height: 118px;
            max-width: 100%;
            object-fit: contain;
            margin: 0 auto 0.25rem auto;
            filter: drop-shadow(0 10px 12px rgba(0, 0, 0, 0.25));
        }

        .player-name {
            color: var(--war-text);
            font-size: 1.08rem;
            font-weight: 800;
            text-align: center;
            margin-top: 0.25rem;
        }

        .player-meta {
            color: var(--war-muted);
            text-align: center;
            font-size: 0.82rem;
            margin-top: 0.2rem;
        }

        .player-stats {
            display: flex;
            justify-content: space-between;
            gap: 0.5rem;
            margin-top: 0.9rem;
        }

        .player-stat {
            flex: 1;
            padding: 0.55rem 0.35rem;
            text-align: center;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.055);
        }

        .player-stat-label {
            color: var(--war-muted);
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .player-stat-value {
            color: var(--war-green);
            font-weight: 800;
            font-size: 0.93rem;
            margin-top: 0.12rem;
        }

        .fixture-pill {
            display: inline-block;
            margin: 0.12rem;
            padding: 0.3rem 0.5rem;
            border-radius: 999px;
            color: #06120e;
            background: var(--war-green);
            font-weight: 800;
            font-size: 0.72rem;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--war-border);
            border-radius: 16px;
            overflow: hidden;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 0.65rem 1rem;
            background: var(--war-panel);
        }

        .stTabs [aria-selected="true"] {
            background: var(--war-purple);
        }

        .stButton > button {
            border-radius: 12px;
            border: 1px solid var(--war-border);
            background: var(--war-panel-soft);
            color: var(--war-text);
        }

        hr {
            border-color: var(--war-border);
        }

        .player-image {
    min-height: 118px;
}

.player-image[alt=""] {
    visibility: hidden;
}
        
        .target-card {
            height: 100%;
            min-height: 255px;
            padding: 1.15rem;
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 18px;
            background:
                linear-gradient(
                    145deg,
                    rgba(139, 92, 246, 0.13),
                    rgba(16, 31, 49, 0.98) 52%
                );
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
        }

        .target-card-top {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .target-rank {
            color: #00ff87;
            font-size: 0.82rem;
            font-weight: 900;
        }

        .target-avatar {
            display: flex;
            width: 48px;
            height: 48px;
            flex: 0 0 48px;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            color: #07121f;
            background: linear-gradient(135deg, #00ff87, #8bffca);
            font-weight: 900;
        }

        .target-identity {
            min-width: 0;
        }

        .target-name {
            overflow: hidden;
            color: #f5f7fb;
            font-size: 1.02rem;
            font-weight: 850;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .target-meta {
            margin-top: 0.15rem;
            color: #9fb0c4;
            font-size: 0.78rem;
        }

        .target-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.45rem;
            margin-top: 1rem;
        }

        .target-metric {
            padding: 0.7rem 0.45rem;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            text-align: center;
        }

        .target-metric span {
            display: block;
            color: #9fb0c4;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .target-metric strong {
            display: block;
            margin-top: 0.2rem;
            color: #00ff87;
            font-size: 0.95rem;
        }

        .target-fixtures {
            margin-top: 0.9rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.07);
        }

        .target-fixtures span {
            color: #9fb0c4;
            font-size: 0.65rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .target-fixtures p {
            margin: 0.25rem 0 0;
            color: #d8e1eb;
            font-size: 0.76rem;
            line-height: 1.4;
        }

        .stTabs [data-baseweb="tab"] {
            color: #aebdd0 !important;
        }

        .stTabs [aria-selected="true"] {
            color: #ffffff !important;
            background: #7048e8 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
