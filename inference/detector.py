import cv2
from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

        # COCO class id for person = 0
        self.PERSON_CLASS_ID = 0

    def detect(self, frame):
        """
        Runs YOLO inference on a single frame.
        Returns list of detections.
        """
        results = self.model(frame, verbose=False)[0]

        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if cls_id == self.PERSON_CLASS_ID and confidence >= self.conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "class": "person",
                    "confidence": round(confidence, 2),
                    "bbox": [x1, y1, x2, y2]
                })

        return detections

    def draw_detections(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = f'Person {det["confidence"]}'

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame, label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 0), 2
            )

        return frame
