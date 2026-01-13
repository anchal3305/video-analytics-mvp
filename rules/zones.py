class Zone:
    def __init__(self, zone_id, name, x1, y1, x2, y2):
        self.zone_id = zone_id
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def contains_bbox(self, bbox):
        """
        bbox = [bx1, by1, bx2, by2]
        Checks if bbox center lies inside zone
        """
        bx1, by1, bx2, by2 = bbox
        cx = (bx1 + bx2) // 2
        cy = (by1 + by2) // 2

        return self.x1 <= cx <= self.x2 and self.y1 <= cy <= self.y2
