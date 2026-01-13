from dataclasses import dataclass
from typing import Optional
import time


@dataclass
class Event:
    camera_id: int
    rule: str
    zone: str
    object_type: str
    confidence: float
    bbox: str               # store as string for SQLite
    timestamp: float = time.time()
    duration_sec: Optional[float] = None
    snapshot_path: Optional[str] = None
