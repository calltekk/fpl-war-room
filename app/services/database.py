from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlalchemy import Engine, text

from ingestion.common.database import create_database_engine


@st.cache_resource
def get_database_engine() -> Engine:
    return create_database_engine()


@st.cache_data(ttl=300)
def read_query(query: str) -> pd.DataFrame:
    engine = get_database_engine()

    with engine.connect() as connection:
        return pd.read_sql_query(
            sql=text(query),
            con=connection,
        )
