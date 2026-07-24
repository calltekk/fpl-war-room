select
    player_id,
    full_name,
    web_name,
    team_name,
    position_short_name,
    current_price,
    selected_by_percent,
    expected_points_next_3,
    expected_points_next_5,
    expected_points_per_million,
    average_difficulty_next_5,
    next_five_opponents,

    round(
        expected_points_next_5
        * greatest(0.10, 1 - selected_by_percent / 100),
        2
    ) as differential_score,

    row_number() over (
        order by
            expected_points_next_5
            * greatest(0.10, 1 - selected_by_percent / 100) desc,
            expected_points_per_million desc
    ) as differential_rank

from {{ ref('player_expected_points_summary') }}

where
    status = 'a'
    and selected_by_percent < 10
    and fixture_count_next_5 > 0
