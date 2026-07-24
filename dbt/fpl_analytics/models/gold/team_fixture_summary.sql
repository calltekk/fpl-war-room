with upcoming as (
    select
        team_id,
        team_name,
        fixture_id,
        event_id,
        opponent_name,
        is_home,
        fixture_difficulty,
        kickoff_time,

        row_number() over (
            partition by team_id
            order by kickoff_time nulls last, fixture_id
        ) as fixture_number

    from {{ ref('team_upcoming_fixtures') }}
    where fixture_status in ('upcoming', 'unscheduled')
),

next_five as (
    select *
    from upcoming
    where fixture_number <= 5
),

summarised as (
    select
        team_id,
        team_name,
        count(*) as upcoming_fixture_count,
        round(avg(fixture_difficulty), 2)
            as average_difficulty_next_five,
        min(fixture_difficulty) as easiest_fixture_rating,
        max(fixture_difficulty) as hardest_fixture_rating,

        string_agg(
            opponent_name
            || case when is_home then ' (H)' else ' (A)' end,
            ', '
            order by fixture_number
        ) as next_five_opponents

    from next_five

    group by
        team_id,
        team_name
)

select
    s.team_id,
    s.team_name,
    t.short_name as team_short_name,
    t.team_code,

    case
        when t.team_code is null then null
        else
            'https://resources.premierleague.com/'
            || 'premierleague/badges/70/t'
            || t.team_code::text
            || '.png'
    end as badge_url,

    s.upcoming_fixture_count,
    s.average_difficulty_next_five,
    s.easiest_fixture_rating,
    s.hardest_fixture_rating,
    s.next_five_opponents

from summarised as s

left join {{ ref('stg_fpl_teams') }} as t
    on s.team_id = t.team_id
