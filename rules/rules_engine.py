import time


class RulesEngine:
    def __init__(self, loitering_threshold_sec=10):
        self.loitering_threshold_sec = loitering_threshold_sec

        # Track how long a person stays in a zone
        # key: (camera_id, zone_id)
        self.zone_entry_times = {}

    def process_detections(self, camera_id, detections, zones):
        """
        Returns list of generated events
        """
        events = []
        current_time = time.time()

        for zone in zones:
            persons_in_zone = [
                det for det in detections
                if zone.contains_bbox(det["bbox"])
            ]

            if persons_in_zone:
                key = (camera_id, zone.zone_id)

                # Intrusion event
                if key not in self.zone_entry_times:
                    self.zone_entry_times[key] = current_time
                    events.append({
                        "camera_id": camera_id,
                        "rule": "intrusion",
                        "zone": zone.name,
                        "timestamp": current_time,
                        "object_type": "person",
                        "confidence": persons_in_zone[0]["confidence"],
                        "bbox": persons_in_zone[0]["bbox"]
                    })

                # Loitering event
                duration = current_time - self.zone_entry_times[key]
                if duration >= self.loitering_threshold_sec:
                    events.append({
                        "camera_id": camera_id,
                        "rule": "loitering",
                        "zone": zone.name,
                        "timestamp": current_time,
                        "object_type": "person",
                        "confidence": persons_in_zone[0]["confidence"],
                        "bbox": persons_in_zone[0]["bbox"],
                        "duration_sec": round(duration, 1)
                    })

            else:
                # Reset if no person in zone
                key = (camera_id, zone.zone_id)
                if key in self.zone_entry_times:
                    del self.zone_entry_times[key]

        return events
