import os
import uuid
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from user_builds import router as user_builds_router
from build_service import check_build_service

app = FastAPI(title="Game10 Backend")

app.include_router(user_builds_router)

DATA = Path(os.getenv("DATA_DIR", "data"))
GAMES = DATA / "games"
GAMES.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    return {
        "app": "Game10 Backend",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/build-service/status")
def build_service_status():
    return check_build_service()


@app.post("/api/games")
def create_game(body: dict):
    name = str(body.get("name", "My Game")).strip()
    html = body.get("html", "")

    if not isinstance(html, str) or not html.strip():
        raise HTTPException(400, "Game HTML is empty")

    if len(html) > 2_000_000:
        raise HTTPException(413, "Game HTML is too large")

    game_id = uuid.uuid4().hex[:12]
    folder = GAMES / game_id
    folder.mkdir(parents=True)

    (folder / "index.html").write_text(
        html, encoding="utf-8"
    )

    record = {
        "id": game_id,
        "name": name,
        "status": "saved"
    }

    (folder / "record.json").write_text(
        json.dumps(record), encoding="utf-8"
    )

    base = os.getenv(
        "PUBLIC_BASE_URL", ""
    ).rstrip("/")

    game_url = (
        f"{base}/games/{game_id}"
        if base else f"/games/{game_id}"
    )

    return {**record, "game_url": game_url}


@app.get("/games/{game_id}", response_class=HTMLResponse)
def get_game(game_id: str):
    file = GAMES / game_id / "index.html"

    if not file.is_file():
        raise HTTPException(404, "Game not found")

    return HTMLResponse(
        file.read_text(encoding="utf-8")
    )


@app.get("/api/games/{game_id}")
def game_record(game_id: str):
    file = GAMES / game_id / "record.json"

    if not file.is_file():
        raise HTTPException(404, "Game not found")

    return json.loads(
        file.read_text(encoding="utf-8")
    )


@app.post("/api/builds")
def request_build(payload: dict):
    provider_url = os.getenv(
        "BUILD_SERVICE_URL", ""
    ).strip()

    if not provider_url:
        raise HTTPException(
            503,
            "APK build provider is not configured."
        )

    raise HTTPException(
        501,
        "Build provider API adapter is not implemented yet."
    )