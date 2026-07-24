select
    team_id,
    trim(team_name) as team_name,
    trim(short_name) as short_name,
    strength,
    ingested_at
from {{ source('bronze', 'fpl_teams') }}
