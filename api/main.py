from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Video Analytics Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP: allow all (OK)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "events.db")

print("API using DB:", DB_PATH)

# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# Camera APIs (MVP – in-memory)
# -------------------------
class CameraIn(BaseModel):
    name: str
    location: str
    rtsp_url: str


class CameraOut(CameraIn):
    id: int
    status: str = "offline"


# Simple in-memory camera store (OK for MVP)
cameras = []


@app.get("/cameras", response_model=List[CameraOut])
def get_cameras():
    return cameras


@app.post("/cameras", response_model=CameraOut)
def add_camera(camera: CameraIn):
    camera_id = len(cameras) + 1
    cam = CameraOut(
        id=camera_id,
        name=camera.name,
        location=camera.location,
        rtsp_url=camera.rtsp_url,
        status="offline"
    )
    cameras.append(cam)
    return cam


# -------------------------
# Event APIs (SQLite-backed)
# -------------------------
@app.get("/events")
def get_events(
    camera_id: Optional[int] = None,
    rule: Optional[str] = None
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if camera_id is not None:
        query += " AND camera_id=?"
        params.append(camera_id)

    if rule is not None:
        query += " AND rule=?"
        params.append(rule)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    events = []
    for r in rows:
        events.append({
            "id": r[0],
            "camera_id": r[1],
            "rule": r[2],
            "zone": r[3],
            "object_type": r[4],
            "confidence": r[5],
            "bbox": r[6],
            "timestamp": r[7],
            "duration_sec": r[8],
            "snapshot_path": r[9]
        })

    return events


@app.get("/events/{event_id}")
def get_event(event_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events WHERE id=?", (event_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Event not found")

    return {
        "id": row[0],
        "camera_id": row[1],
        "rule": row[2],
        "zone": row[3],
        "object_type": row[4],
        "confidence": row[5],
        "bbox": row[6],
        "timestamp": row[7],
        "duration_sec": row[8],
        "snapshot_path": row[9]
    }
