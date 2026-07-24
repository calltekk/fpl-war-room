CREATE TABLE IF NOT EXISTS bronze.fpl_players (
    player_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    second_name TEXT NOT NULL,
    web_name TEXT NOT NULL,
    team_id INTEGER NOT NULL,
    position_id INTEGER NOT NULL,
    current_price NUMERIC(6, 1) NOT NULL,
    total_points INTEGER NOT NULL,
    selected_by_percent NUMERIC(6, 2),
    status TEXT,
    raw_payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bronze.fpl_teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    strength INTEGER,
    raw_payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bronze.fpl_events (
    event_id INTEGER PRIMARY KEY,
    event_name TEXT NOT NULL,
    deadline_time TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL,
    is_next BOOLEAN NOT NULL,
    is_previous BOOLEAN NOT NULL,
    raw_payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
