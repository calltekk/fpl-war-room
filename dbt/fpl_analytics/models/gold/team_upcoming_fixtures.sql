with home_fixtures as (
    select
        fixture_id,
        event_id,
        event_name,
        kickoff_time,
        team_home_id as team_id,
        home_team_name as team_name,
        away_team_name as opponent_name,
        true as is_home,
        team_home_difficulty as fixture_difficulty,
        fixture_status
    from {{ ref('fct_fixtures') }}
),

away_fixtures as (
    select
        fixture_id,
        event_id,
        event_name,
        kickoff_time,
        team_away_id as team_id,
        away_team_name as team_name,
        home_team_name as opponent_name,
        false as is_home,
        team_away_difficulty as fixture_difficulty,
        fixture_status
    from {{ ref('fct_fixtures') }}
),

combined as (
    select * from home_fixtures
    union all
    select * from away_fixtures
)

select
    fixture_id,
    event_id,
    event_name,
    kickoff_time,
    team_id,
    team_name,
    opponent_name,
    is_home,
    fixture_difficulty,
    fixture_status
from combined
