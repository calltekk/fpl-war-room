select
    p.player_id,
    p.first_name,
    p.second_name,
    p.full_name,
    p.web_name,
    p.team_id,
    t.team_name,
    t.short_name as team_short_name,
    p.position_id,
    pos.position_name,
    pos.position_short_name,
    p.current_price,
    p.total_points,
    p.selected_by_percent,
    p.status,
    p.ingested_at
from {{ ref('stg_fpl_players') }} as p

left join {{ ref('stg_fpl_teams') }} as t
    on p.team_id = t.team_id

left join {{ ref('player_positions') }} as pos
    on p.position_id = pos.position_id
