import cv2
import time
from ingestion.camera import Camera
from inference.detector import YOLODetector


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

        self.cap = None
        self.detector = YOLODetector(conf_threshold=0.5)

        self.frame_count = 0
        self.last_detections = []

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

                # Run YOLO every N frames
                if self.frame_count % self.detect_every_n_frames == 0:
                    self.last_detections = self.detector.detect(frame)

                # Draw detections
                frame = self.detector.draw_detections(frame, self.last_detections)

                # FPS calculation
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
