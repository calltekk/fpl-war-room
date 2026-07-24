select
    event_id,
    event_name,
    deadline_time,
    is_current,
    is_next,
    is_previous,
    ingested_at
from {{ source('bronze', 'fpl_events') }}
