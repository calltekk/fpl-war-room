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
    total_points,
    selected_by_percent,
    status,

    round(
        total_points / nullif(current_price, 0),
        2
    ) as points_per_million,

    row_number() over (
        partition by position_id
        order by
            total_points / nullif(current_price, 0) desc,
            total_points desc
    ) as value_rank_by_position,

    row_number() over (
        order by
            total_points / nullif(current_price, 0) desc,
            total_points desc
    ) as overall_value_rank

from {{ ref('dim_players') }}
where current_price > 0
