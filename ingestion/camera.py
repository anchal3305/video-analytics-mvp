from datetime import datetime

class Camera:
    def __init__(self, camera_id, name, location, rtsp_url):
        self.camera_id = camera_id
        self.name = name
        self.location = location
        self.rtsp_url = rtsp_url

        self.status = "offline"
        self.fps = 0.0
        self.last_frame_time = None

    def mark_online(self):
        self.status = "online"
        self.last_frame_time = datetime.utcnow()

    def mark_offline(self):
        self.status = "offline"

    def update_fps(self, fps):
        self.fps = round(fps, 2)

    def to_dict(self):
        return {
            "camera_id": self.camera_id,
            "name": self.name,
            "location": self.location,
            "rtsp_url": self.rtsp_url,
            "status": self.status,
            "fps": self.fps,
            "last_frame_time": self.last_frame_time.isoformat()
            if self.last_frame_time else None,
        }
