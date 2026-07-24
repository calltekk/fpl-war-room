select
    p.player_id,
    p.full_name,
    p.web_name,
    p.team_name,
    p.position_name,
    p.position_short_name,
    p.current_price,
    p.total_points,
    p.points_per_million,
    p.selected_by_percent,
    p.status,
    p.value_rank_by_position,

    f.average_difficulty_next_five,
    f.next_five_opponents,

    case
        when p.selected_by_percent < 5 then 'Differential'
        when p.selected_by_percent < 15 then 'Moderate ownership'
        else 'Highly owned'
    end as ownership_category,

    case
        when f.average_difficulty_next_five <= 2.5 then 'Excellent'
        when f.average_difficulty_next_five <= 3.0 then 'Good'
        when f.average_difficulty_next_five <= 3.5 then 'Average'
        else 'Difficult'
    end as fixture_outlook

from {{ ref('player_value_rankings') }} as p

left join {{ ref('team_fixture_summary') }} as f
    on p.team_id = f.team_id

where p.status = 'a'
