select
    f.fixture_id,
    f.event_id,
    e.event_name,
    f.kickoff_time,

    f.team_home_id,
    home_team.team_name as home_team_name,
    home_team.short_name as home_team_short_name,

    f.team_away_id,
    away_team.team_name as away_team_name,
    away_team.short_name as away_team_short_name,

    f.team_home_score,
    f.team_away_score,
    f.team_home_difficulty,
    f.team_away_difficulty,

    f.finished,
    f.started,
    f.provisional_start_time,
    f.minutes,

    case
        when f.finished then 'finished'
        when f.started then 'live'
        when f.kickoff_time is null then 'unscheduled'
        else 'upcoming'
    end as fixture_status,

    f.ingested_at
from {{ ref('stg_fpl_fixtures') }} as f

left join {{ ref('stg_fpl_events') }} as e
    on f.event_id = e.event_id

left join {{ ref('stg_fpl_teams') }} as home_team
    on f.team_home_id = home_team.team_id

left join {{ ref('stg_fpl_teams') }} as away_team
    on f.team_away_id = away_team.team_id
