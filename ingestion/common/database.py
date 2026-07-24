from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import Connection


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")

    @property
    def sqlalchemy_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


def create_database_engine(settings: DatabaseSettings | None = None) -> Engine:
    resolved_settings = settings or DatabaseSettings()  # type: ignore[call-arg]

    return create_engine(
        resolved_settings.sqlalchemy_url,
        pool_pre_ping=True,
    )


@contextmanager
def database_connection(engine: Engine) -> Iterator[Connection]:
    with engine.begin() as connection:
        yield connection
