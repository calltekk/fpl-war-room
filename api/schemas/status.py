from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class DataRefreshStatus(BaseModel):
    last_successful_refresh: datetime | None
    latest_pipeline: str | None
    records_loaded: int | None
