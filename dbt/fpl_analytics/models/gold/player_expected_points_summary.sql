with projections as (
    select *
    from {{ ref('player_expected_points') }}
),

summarised as (
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

        round(
            sum(expected_points)
                filter (where fixture_number <= 3),
            2
        ) as expected_points_next_3,

        round(
            sum(expected_points)
                filter (where fixture_number <= 5),
            2
        ) as expected_points_next_5,

        round(
            avg(fixture_difficulty)
                filter (where fixture_number <= 5),
            2
        ) as average_difficulty_next_5,

        count(*)
            filter (where fixture_number <= 3) as fixture_count_next_3,

        count(*)
            filter (where fixture_number <= 5) as fixture_count_next_5,

        string_agg(
            opponent_name
            || case when is_home then ' (H)' else ' (A)' end,
            ', '
            order by fixture_number
        ) filter (
            where fixture_number <= 5
        ) as next_five_opponents

    from projections

    group by
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
        status
)

select
    *,

    round(
        expected_points_next_5 / nullif(current_price, 0),
        2
    ) as expected_points_per_million,

    row_number() over (
        partition by position_id
        order by
            expected_points_next_5 desc,
            current_price asc
    ) as expected_points_rank_by_position,

    row_number() over (
        order by
            expected_points_next_5 desc,
            current_price asc
    ) as expected_points_rank_overall

from summarised
