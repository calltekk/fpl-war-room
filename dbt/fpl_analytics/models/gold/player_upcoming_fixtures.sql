with player_fixtures as (
    select
        p.player_id,
        p.full_name,
        p.web_name,
        p.team_id,
        p.team_name,
        p.team_short_name,
        p.position_id,
        p.position_name,
        p.position_short_name,
        p.current_price,
        p.selected_by_percent,
        p.status,

        f.fixture_id,
        f.event_id,
        f.event_name,
        f.kickoff_time,
        f.opponent_name,
        f.is_home,
        f.fixture_difficulty,

        row_number() over (
            partition by p.player_id
            order by
                f.kickoff_time nulls last,
                f.fixture_id
        ) as fixture_number

    from {{ ref('dim_players') }} as p

    inner join {{ ref('team_upcoming_fixtures') }} as f
        on p.team_id = f.team_id

    where f.fixture_status in ('upcoming', 'unscheduled')
)

select *
from player_fixtures
