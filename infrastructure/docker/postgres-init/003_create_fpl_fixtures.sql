CREATE TABLE IF NOT EXISTS bronze.fpl_fixtures (
    fixture_id INTEGER PRIMARY KEY,
    event_id INTEGER,
    kickoff_time TIMESTAMPTZ,
    team_home_id INTEGER NOT NULL,
    team_away_id INTEGER NOT NULL,
    team_home_score INTEGER,
    team_away_score INTEGER,
    team_home_difficulty INTEGER,
    team_away_difficulty INTEGER,
    finished BOOLEAN NOT NULL,
    started BOOLEAN NOT NULL,
    provisional_start_time BOOLEAN NOT NULL,
    minutes INTEGER NOT NULL,
    raw_payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fixture_teams_different
        CHECK (team_home_id <> team_away_id)
);

CREATE INDEX IF NOT EXISTS idx_fpl_fixtures_event_id
    ON bronze.fpl_fixtures (event_id);

CREATE INDEX IF NOT EXISTS idx_fpl_fixtures_kickoff_time
    ON bronze.fpl_fixtures (kickoff_time);

CREATE INDEX IF NOT EXISTS idx_fpl_fixtures_home_team
    ON bronze.fpl_fixtures (team_home_id);

CREATE INDEX IF NOT EXISTS idx_fpl_fixtures_away_team
    ON bronze.fpl_fixtures (team_away_id);
