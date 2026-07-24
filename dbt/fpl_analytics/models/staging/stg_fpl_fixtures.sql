select
    fixture_id,
    event_id,
    kickoff_time,
    team_home_id,
    team_away_id,
    team_home_score,
    team_away_score,
    team_home_difficulty,
    team_away_difficulty,
    finished,
    started,
    provisional_start_time,
    minutes,
    ingested_at
from {{ source('bronze', 'fpl_fixtures') }}
