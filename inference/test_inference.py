import os
import cv2
from detector import YOLODetector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "test.jpg")

image = cv2.imread(image_path)

if image is None:
    raise Exception("Could not load image. Check path.")

detector = YOLODetector(conf_threshold=0.5)

detections = detector.detect(image)
print("Detections:", detections)

annotated = detector.draw_detections(image, detections)

cv2.imshow("YOLO Test", annotated)
cv2.imwrite(os.path.join(BASE_DIR, "output.jpg"), annotated)

cv2.waitKey(0)
cv2.destroyAllWindows()
