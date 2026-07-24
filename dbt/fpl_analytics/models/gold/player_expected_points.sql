with player_fixtures as (
    select *
    from {{ ref('player_upcoming_fixtures') }}
),

scored as (
    select
        *,

        case position_id
            when 1 then 2.4
            when 2 then 2.6
            when 3 then 3.0
            when 4 then 3.2
            else 2.0
        end as position_base_points,

        case fixture_difficulty
            when 1 then 1.45
            when 2 then 1.22
            when 3 then 1.00
            when 4 then 0.82
            when 5 then 0.66
            else 0.90
        end as fixture_multiplier,

        case
            when is_home then 1.08
            else 0.95
        end as venue_multiplier,

        case status
            when 'a' then 1.00
            when 'd' then 0.72
            when 'i' then 0.18
            when 's' then 0.00
            when 'u' then 0.35
            else 0.75
        end as availability_multiplier,

        least(
            1.18,
            greatest(
                0.82,
                0.90 + (current_price - 4.5) * 0.025
            )
        ) as price_quality_multiplier,

        least(
            1.10,
            greatest(
                0.90,
                0.94 + selected_by_percent * 0.002
            )
        ) as ownership_confidence_multiplier

    from player_fixtures
),

projected as (
    select
        *,

        round(
            position_base_points
            * fixture_multiplier
            * venue_multiplier
            * availability_multiplier
            * price_quality_multiplier
            * ownership_confidence_multiplier,
            2
        ) as expected_points

    from scored
)

select
    player_id,
    full_name,
    web_name,
    team_id,
    team_name,
    team_short_name,
    position_id,
    position_name,
    position_short_name,
    current_price,
    selected_by_percent,
    status,

    fixture_id,
    event_id,
    event_name,
    kickoff_time,
    opponent_name,
    is_home,
    fixture_difficulty,
    fixture_number,

    position_base_points,
    fixture_multiplier,
    venue_multiplier,
    availability_multiplier,
    price_quality_multiplier,
    ownership_confidence_multiplier,

    expected_points

from projected
