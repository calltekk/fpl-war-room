from __future__ import annotations

from typing import Any, cast

import httpx
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from tenacity import retry, stop_after_attempt, wait_exponential


class FPLSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = Field(
        default="https://fantasy.premierleague.com/api",
        alias="FPL_BASE_URL",
    )


class FPLClient:
    def __init__(
        self,
        settings: FPLSettings | None = None,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.settings = settings or FPLSettings()
        self.client = httpx.Client(
            base_url=self.settings.base_url,
            timeout=timeout_seconds,
            headers={
                "User-Agent": "fpl-war-room/0.1",
                "Accept": "application/json",
            },
        )

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> FPLClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    def get_bootstrap_static(self) -> dict[str, Any]:
        response = self.client.get("/bootstrap-static/")
        response.raise_for_status()

        payload: object = response.json()

        if not isinstance(payload, dict):
            raise TypeError("FPL bootstrap response was not a JSON object")

        return cast(dict[str, Any], payload)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    def get_fixtures(self) -> list[dict[str, Any]]:
        response = self.client.get("/fixtures/")
        response.raise_for_status()

        payload: object = response.json()

        if not isinstance(payload, list):
            raise TypeError("FPL fixtures response was not a JSON array")

        if not all(isinstance(item, dict) for item in payload):
            raise TypeError("FPL fixtures response contained an invalid record")

        return cast(list[dict[str, Any]], payload)
