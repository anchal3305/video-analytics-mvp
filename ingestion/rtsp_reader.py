import cv2
import time
from camera import Camera


class RTSPReader:
    def __init__(self, camera: Camera, reconnect_delay=5):
        self.camera = camera
        self.reconnect_delay = reconnect_delay
        self.cap = None

    def connect(self):
        print(f"[INFO] Connecting to camera: {self.camera.name}")
        self.cap = cv2.VideoCapture(self.camera.rtsp_url)

        if not self.cap.isOpened():
            print("[ERROR] Failed to connect to stream")
            self.camera.mark_offline()
            return False

        self.camera.mark_online()
        print("[INFO] Camera connected")
        return True

    def start(self):
        frame_count = 0
        start_time = time.time()

        while True:
            if self.cap is None or not self.cap.isOpened():
                self.camera.mark_offline()
                time.sleep(self.reconnect_delay)
                self.connect()
                continue

            ret, frame = self.cap.read()

            if not ret:
                print("[WARN] Frame read failed. Reconnecting...")
                self.cap.release()
                self.cap = None
                continue

            frame_count += 1
            elapsed = time.time() - start_time

            if elapsed >= 1.0:
                fps = frame_count / elapsed
                self.camera.update_fps(fps)
                frame_count = 0
                start_time = time.time()

                print(
                    f"[{self.camera.name}] "
                    f"Status: {self.camera.status} | "
                    f"FPS: {self.camera.fps}"
                )

            self.camera.last_frame_time = time.time()

            # TEMP: show frame (for testing only)
            cv2.imshow(self.camera.name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

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

    reader = RTSPReader(camera)
    reader.connect()
    reader.start()
