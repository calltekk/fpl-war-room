from __future__ import annotations

import httpx
import respx

from ingestion.fpl.client import FPLClient, FPLSettings


@respx.mock
def test_get_bootstrap_static() -> None:
    route = respx.get("https://fantasy.premierleague.com/api/bootstrap-static/").mock(
        return_value=httpx.Response(
            200,
            json={
                "elements": [],
                "teams": [],
                "events": [],
            },
        )
    )

    with FPLClient(settings=FPLSettings()) as client:
        result = client.get_bootstrap_static()

    assert route.called
    assert result["elements"] == []


@respx.mock
def test_get_fixtures() -> None:
    route = respx.get("https://fantasy.premierleague.com/api/fixtures/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": 1,
                    "team_h": 1,
                    "team_a": 2,
                }
            ],
        )
    )

    with FPLClient(settings=FPLSettings()) as client:
        result = client.get_fixtures()

    assert route.called
    assert len(result) == 1
    assert result[0]["id"] == 1
