from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.fixtures import router as fixtures_router
from api.routes.players import router as players_router
from api.routes.status import router as status_router

app = FastAPI(
    title="FPL War Room API",
    version="0.1.0",
    description="API layer for FPL analytics and recommendations.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players_router)
app.include_router(fixtures_router)
app.include_router(status_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
