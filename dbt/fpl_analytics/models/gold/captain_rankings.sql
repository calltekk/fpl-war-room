select
    player_id,
    full_name,
    web_name,
    team_name,
    team_short_name,
    team_code,
    badge_url,
    position_short_name,
    current_price,
    selected_by_percent,
    expected_points_next_3,
    expected_points_next_5,
    expected_points_per_million,
    average_difficulty_next_5,
    next_five_opponents,

    round(expected_points_next_3 * 2, 2) as captain_points_next_3,

    row_number() over (
        order by
            expected_points_next_3 desc,
            selected_by_percent desc
    ) as captain_rank

from {{ ref('player_expected_points_summary') }}

where
    status = 'a'
    and fixture_count_next_3 > 0
