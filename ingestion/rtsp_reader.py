import cv2
import time

from ingestion.camera import Camera
from inference.detector import YOLODetector
from rules.zones import Zone
from rules.rules_engine import RulesEngine


class RTSPReader:
    def __init__(
        self,
        camera: Camera,
        detect_every_n_frames=5,
        reconnect_delay=5
    ):
        self.camera = camera
        self.reconnect_delay = reconnect_delay
        self.detect_every_n_frames = detect_every_n_frames

        # Video + inference
        self.cap = None
        self.detector = YOLODetector(conf_threshold=0.5)

        self.frame_count = 0
        self.last_detections = []

        # 🔹 Rules engine
        self.rules_engine = RulesEngine(loitering_threshold_sec=10)

        # 🔹 Zones (hardcoded MVP)
        self.zones = [
            Zone(
                zone_id=1,
                name="Restricted Area",
                x1=200,
                y1=200,
                x2=600,
                y2=600
            )
        ]

    def connect(self):
        print(f"[INFO] Connecting to camera: {self.camera.name}")
        self.cap = cv2.VideoCapture(self.camera.rtsp_url, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print("[ERROR] Failed to connect to stream")
            self.camera.mark_offline()
            return False

        self.camera.mark_online()
        print("[INFO] Camera connected")
        return True

    def start(self):
        fps_frame_count = 0
        fps_start_time = time.time()

        try:
            while True:
                if self.cap is None or not self.cap.isOpened():
                    self.camera.mark_offline()
                    time.sleep(self.reconnect_delay)
                    self.connect()
                    continue

                ret, frame = self.cap.read()
                if not ret or frame is None:
                    print("[WARN] Frame read failed. Reconnecting...")
                    if self.cap:
                        self.cap.release()
                    self.cap = None
                    continue

                self.frame_count += 1
                fps_frame_count += 1

                # 🔹 YOLO inference every N frames
                if self.frame_count % self.detect_every_n_frames == 0:
                    self.last_detections = self.detector.detect(frame)

                # 🔹 Draw detections
                frame = self.detector.draw_detections(frame, self.last_detections)

                # 🔹 Process rules
                events = self.rules_engine.process_detections(
                    camera_id=self.camera.camera_id,
                    detections=self.last_detections,
                    zones=self.zones
                )

                for event in events:
                    print("[EVENT]", event)

                # 🔹 Draw zones
                for zone in self.zones:
                    cv2.rectangle(
                        frame,
                        (zone.x1, zone.y1),
                        (zone.x2, zone.y2),
                        (255, 0, 0),
                        2
                    )
                    cv2.putText(
                        frame,
                        zone.name,
                        (zone.x1, zone.y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 0, 0),
                        2
                    )

                # 🔹 FPS calculation
                elapsed = time.time() - fps_start_time
                if elapsed >= 1.0:
                    fps = fps_frame_count / elapsed
                    self.camera.update_fps(fps)
                    fps_frame_count = 0
                    fps_start_time = time.time()

                    print(
                        f"[{self.camera.name}] "
                        f"Status: {self.camera.status} | "
                        f"FPS: {self.camera.fps} | "
                        f"Detections: {len(self.last_detections)}"
                    )

                self.camera.last_frame_time = time.time()

                cv2.imshow(self.camera.name, frame)

                # ✅ Reliable exit
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("[INFO] 'q' pressed. Exiting...")
                    break

        except KeyboardInterrupt:
            print("\n[INFO] Keyboard interrupt received. Exiting...")

        finally:
            self.stop()

    def stop(self):
        print("[INFO] Stopping stream")
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    camera = Camera(
        camera_id=1,
        name="Test Camera",
        location="Local",
        rtsp_url=1  # webcam
    )

    reader = RTSPReader(camera, detect_every_n_frames=5)
    reader.connect()
    reader.start()
