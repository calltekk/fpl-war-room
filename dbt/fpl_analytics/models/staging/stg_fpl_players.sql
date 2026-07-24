select
    player_id,
    player_code,
    photo_filename,
    trim(first_name) as first_name,
    trim(second_name) as second_name,
    trim(first_name || ' ' || second_name) as full_name,
    trim(web_name) as web_name,
    team_id,
    position_id,
    current_price,
    total_points,
    selected_by_percent,
    status,
    ingested_at
from {{ source('bronze', 'fpl_players') }}
