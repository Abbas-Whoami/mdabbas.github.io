"""Vehicle classification module using YOLOv8 object detection."""

import os

from src.config import (
    YOLO_MODEL_PATH,
    YOLO_CONFIDENCE_THRESHOLD,
)


class VehicleClassifier:
    """Classifies detected vehicles using YOLOv8 (via ultralytics)."""

    # COCO class IDs for vehicles
    VEHICLE_CLASS_MAP = {
        1: "Bicycle",
        2: "Car",
        3: "Motorcycle",
        5: "Bus",
        7: "Truck",
    }

    def __init__(self, model_path=None):
        """
        Initialize the YOLO classifier.

        Args:
            model_path: Path to the YOLOv8 .pt model file.
        """
        self.model_path = model_path or YOLO_MODEL_PATH
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the YOLOv8 model using ultralytics."""
        if not os.path.exists(self.model_path):
            print(f"Warning: YOLO model not found at '{self.model_path}'")
            print("Run 'python download_model.py' to download it.")
            print("Using size-based fallback classification.")
            return

        try:
            import torch

            # Fix for PyTorch 2.6+ weights_only default
            _original_load = torch.load

            def _patched_load(*args, **kwargs):
                kwargs.setdefault("weights_only", False)
                return _original_load(*args, **kwargs)

            torch.load = _patched_load

            from ultralytics import YOLO

            self.model = YOLO(self.model_path)
            torch.load = _original_load

            print(f"YOLO model loaded: {self.model_path}")

        except ImportError:
            print("Warning: 'ultralytics' package not installed.")
            print("Install with: pip install ultralytics")
            print("Using size-based fallback classification.")
            self.model = None

    def detect_and_classify(self, frame):
        """
        Run YOLO detection on the frame and return classified vehicles.

        Args:
            frame: BGR image (numpy array).

        Returns:
            List of tuples [(x, y, w, h, class_name, confidence), ...]
        """
        if self.model is None:
            return []

        # Run inference (only detect vehicle classes)
        results = self.model(
            frame,
            conf=YOLO_CONFIDENCE_THRESHOLD,
            classes=list(self.VEHICLE_CLASS_MAP.keys()),
            verbose=False,
        )

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                # Get bounding box in xyxy format
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                w = x2 - x1
                h = y2 - y1

                # Get class and confidence
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                class_name = self.VEHICLE_CLASS_MAP.get(class_id, "Unknown")

                detections.append((x1, y1, w, h, class_name, confidence))

        return detections

    def classify_by_bbox(self, frame, bbox):
        """
        Classify a single vehicle given its bounding box region.

        Args:
            frame: Full BGR frame.
            bbox: Bounding box (x, y, w, h).

        Returns:
            Vehicle class name string.
        """
        if self.model is None:
            return self._fallback_classify(bbox)

        x, y, w, h = bbox

        # Expand the crop slightly for better detection
        pad = 20
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(frame.shape[1], x + w + pad)
        y2 = min(frame.shape[0], y + h + pad)

        crop = frame[y1:y2, x1:x2]

        if crop.size == 0:
            return self._fallback_classify(bbox)

        detections = self.detect_and_classify(crop)

        if detections:
            # Return the class with highest confidence
            best = max(detections, key=lambda d: d[5])
            return best[4]

        return self._fallback_classify(bbox)

    @staticmethod
    def _fallback_classify(bbox):
        """
        Fallback classification based on bounding box aspect ratio and size.

        Args:
            bbox: Bounding box (x, y, w, h).

        Returns:
            Estimated vehicle class name.
        """
        _, _, w, h = bbox
        area = w * h
        aspect_ratio = w / max(h, 1)

        if area < 3000:
            return "Motorcycle"
        elif area < 8000:
            if aspect_ratio < 1.2:
                return "Motorcycle"
            else:
                return "Car"
        elif area < 25000:
            return "Car"
        elif area < 50000:
            if aspect_ratio > 2.0:
                return "Bus"
            else:
                return "Truck"
        else:
            return "Truck"
