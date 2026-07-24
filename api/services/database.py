from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import RowMapping

from ingestion.common.database import create_database_engine


def fetch_all(query: str) -> Sequence[RowMapping]:
    engine = create_database_engine()

    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.mappings().all()


def fetch_one(query: str) -> dict[str, Any] | None:
    rows = fetch_all(query)

    if not rows:
        return None

    return dict(rows[0])
