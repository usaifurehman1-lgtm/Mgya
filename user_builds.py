import os
import sqlite3
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/user-builds",
    tags=["User Builds"]
)

DATA = Path(os.getenv("DATA_DIR", "data"))
DATA.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA / "user_builds.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS build_requests (
                request_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                project_name TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)


init_db()


class BuildRequest(BaseModel):
    user_id: str
    project_name: str


@router.post("/")
def create_build_request(body: BuildRequest):
    user_id = body.user_id.strip()
    project_name = body.project_name.strip()

    if not user_id or not project_name:
        raise HTTPException(
            400,
            "User ID and project name are required."
        )

    request_id = uuid.uuid4().hex[:12]

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO build_requests
            (request_id, user_id, project_name, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                request_id,
                user_id,
                project_name,
                "queued"
            )
        )

    return {
        "request_id": request_id,
        "user_id": user_id,
        "project_name": project_name,
        "status": "queued",
        "message": (
            "Request saved. A real APK build provider "
            "must be connected to build the APK."
        )
    }


@router.get("/{user_id}")
def get_user_builds(user_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT request_id, project_name, status
            FROM build_requests
            WHERE user_id = ?
            """,
            (user_id.strip(),)
        ).fetchall()

    return {
        "user_id": user_id,
        "builds": [
            {
                "request_id": row[0],
                "project_name": row[1],
                "status": row[2]
            }
            for row in rows
        ]
    }