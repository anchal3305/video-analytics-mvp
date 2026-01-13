import sqlite3
import os
from events.models import Event

# 🔑 SINGLE SOURCE OF TRUTH FOR DB LOCATION
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "events.db")


class EventStore:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        print("EventStore DB Path:", self.db_path)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id INTEGER,
            rule TEXT,
            zone TEXT,
            object_type TEXT,
            confidence REAL,
            bbox TEXT,
            timestamp REAL,
            duration_sec REAL,
            snapshot_path TEXT
        )
        """)

        conn.commit()
        conn.close()

    def insert_event(self, event: Event):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO events (
            camera_id, rule, zone, object_type,
            confidence, bbox, timestamp, duration_sec, snapshot_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.camera_id,
            event.rule,
            event.zone,
            event.object_type,
            event.confidence,
            event.bbox,
            event.timestamp,
            event.duration_sec,
            event.snapshot_path
        ))

        conn.commit()
        conn.close()

    def fetch_events(self, camera_id=None, rule=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM events WHERE 1=1"
        params = []

        if camera_id:
            query += " AND camera_id=?"
            params.append(camera_id)

        if rule:
            query += " AND rule=?"
            params.append(rule)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
