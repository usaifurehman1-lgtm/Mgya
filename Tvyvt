import os, uuid, json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Game10 Backend")
DATA = Path(os.getenv("DATA_DIR", "data"))
GAMES = DATA / "games"
GAMES.mkdir(parents=True, exist_ok=True)

class GameInput(BaseModel):
    name: str = "My Game"
    html: str

@app.get("/")
def home():
    return {"app": "Game10 Backend", "status": "running"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/games")
def create_game(body: GameInput):
    if not body.html.strip():
        raise HTTPException(400, "Game HTML is empty")
    if len(body.html) > 2_000_000:
        raise HTTPException(413, "Game HTML is too large")
    game_id = uuid.uuid4().hex[:12]
    folder = GAMES / game_id
    folder.mkdir(parents=True)
    (folder / "index.html").write_text(body.html, encoding="utf-8")
    record = {"id": game_id, "name": body.name, "status": "saved"}
    (folder / "record.json").write_text(json.dumps(record), encoding="utf-8")
    base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    return {**record, "game_url": f"{base}/games/{game_id}" if base else f"/games/{game_id}"}

@app.get("/games/{game_id}", response_class=HTMLResponse)
def get_game(game_id: str):
    file = GAMES / game_id / "index.html"
    if not file.is_file():
        raise HTTPException(404, "Game not found")
    return HTMLResponse(file.read_text(encoding="utf-8"))

@app.get("/api/games/{game_id}")
def game_record(game_id: str):
    file = GAMES / game_id / "record.json"
    if not file.is_file():
        raise HTTPException(404, "Game not found")
    return json.loads(file.read_text(encoding="utf-8"))

@app.post("/api/builds")
def request_build(payload: dict):
    # No fake success: a real Android build provider must be connected.
    provider_url = os.getenv("BUILD_SERVICE_URL", "").strip()
    if not provider_url:
        raise HTTPException(
            503,
            "APK build provider is not configured. Connect a real Android build service first."
        )
    raise HTTPException(
        501,
        "Build provider URL is set, but its API adapter is not implemented yet."
    )
