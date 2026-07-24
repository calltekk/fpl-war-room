from __future__ import annotations

from fastapi import APIRouter

from api.schemas.status import DataRefreshStatus
from api.services.database import fetch_one

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/data-refresh", response_model=DataRefreshStatus)
def get_data_refresh_status() -> DataRefreshStatus:
    row = fetch_one(
        """
        select
            completed_at as last_successful_refresh,
            pipeline_name as latest_pipeline,
            records_loaded
        from audit.pipeline_runs
        where status = 'SUCCESS'
        order by completed_at desc nulls last
        limit 1
        """
    )

    if row is None:
        return DataRefreshStatus(
            last_successful_refresh=None,
            latest_pipeline=None,
            records_loaded=None,
        )

    return DataRefreshStatus(**row)
