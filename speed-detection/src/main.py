"""Main module for the vehicle speed detection system."""

import cv2

from src.vehicle_detector import VehicleDetector
from src.vehicle_classifier import VehicleClassifier
from src.vehicle_tracker import VehicleTracker
from src.speed_estimator import SpeedEstimator
from src.config import (
    FRAME_WIDTH,
    FRAME_HEIGHT,
    MAX_DISTANCE_THRESHOLD,
    MAX_FRAMES_TO_SKIP,
    YOLO_MODEL_PATH,
    VEHICLE_COLORS,
    SPEED_TEXT_COLOR,
    FONT_SCALE,
    FONT_THICKNESS,
    ROI_Y_START,
    ROI_Y_END,
)


class VehicleSpeedDetectionSystem:
    """Main system class that orchestrates detection, tracking, and speed estimation."""

    def __init__(self, video_path, output_path=None):
        """
        Initialize the vehicle speed detection system.

        Args:
            video_path: Path to the input MP4 video file.
            output_path: Optional path to save the processed video.
        """
        self.video_path = video_path
        self.output_path = output_path

        # Initialize components
        self.detector = VehicleDetector()
        self.classifier = VehicleClassifier(model_path=YOLO_MODEL_PATH)
        self.tracker = VehicleTracker(
            max_distance=MAX_DISTANCE_THRESHOLD,
            max_frames_to_skip=MAX_FRAMES_TO_SKIP,
        )
        self.speed_estimator = SpeedEstimator()

        # Video capture
        self.capture = None
        self.writer = None
        self.fps = 30
        self.frame_count = 0

    def initialize_video(self):
        """Open the video file and initialize the video writer if needed."""
        self.capture = cv2.VideoCapture(self.video_path)

        if not self.capture.isOpened():
            raise FileNotFoundError(
                f"Cannot open video file: {self.video_path}"
            )

        # Get video properties
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS)) or 30
        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Update speed estimator with actual FPS
        self.speed_estimator.update_fps(self.fps)

        print(f"Video loaded: {width}x{height} @ {self.fps} FPS")

        # Initialize video writer for output
        if self.output_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(
                self.output_path, fourcc, self.fps, (width, height)
            )

    def process_frame(self, frame):
        """
        Process a single video frame.

        Args:
            frame: BGR image (numpy array).

        Returns:
            Annotated frame with bounding boxes, vehicle types, and speed labels.
        """
        # Detect vehicles using background subtraction
        detections = self.detector.detect(frame)

        # Update tracker
        tracked_vehicles = self.tracker.update(detections)

        # Classify vehicles using YOLO (run every 5 frames for performance)
        if self.frame_count % 5 == 0:
            yolo_detections = self.classifier.detect_and_classify(frame)
            self._match_classifications(tracked_vehicles, yolo_detections)

        # Estimate speed and annotate frame
        for vehicle_id, vehicle in tracked_vehicles.items():
            speed = self.speed_estimator.estimate_speed(vehicle)
            vehicle.estimated_speed = speed

            # If vehicle type is still unknown, use fallback
            if vehicle.vehicle_type == "Unknown" and vehicle.bbox is not None:
                vehicle.vehicle_type = self.classifier._fallback_classify(
                    vehicle.bbox
                )

            # Get color based on vehicle type
            color = VEHICLE_COLORS.get(vehicle.vehicle_type, (255, 255, 255))

            # Draw bounding box
            if vehicle.bbox is not None:
                x, y, w, h = vehicle.bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                # Draw vehicle type and speed label
                label = f"{vehicle.vehicle_type} | {speed:.1f} km/h"
                label_id = f"ID: {vehicle_id}"

                # Background rectangle for text readability
                text_size = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS
                )[0]
                cv2.rectangle(
                    frame,
                    (x, y - 35),
                    (x + text_size[0] + 5, y - 5),
                    color, -1
                )

                cv2.putText(
                    frame, label, (x + 2, y - 18),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SCALE, (0, 0, 0), FONT_THICKNESS,
                )
                cv2.putText(
                    frame, label_id, (x + 2, y + h + 18),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1,
                )

        # Draw ROI lines
        cv2.line(frame, (0, ROI_Y_START), (frame.shape[1], ROI_Y_START),
                 (255, 0, 0), 1)
        cv2.line(frame, (0, ROI_Y_END), (frame.shape[1], ROI_Y_END),
                 (255, 0, 0), 1)

        # Draw frame info and legend
        cv2.putText(
            frame,
            f"Frame: {self.frame_count} | Vehicles: {len(tracked_vehicles)}",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
        )

        # Draw legend
        self._draw_legend(frame)

        return frame

    def _match_classifications(self, tracked_vehicles, yolo_detections):
        """
        Match YOLO classifications to tracked vehicles based on IoU overlap.

        Args:
            tracked_vehicles: Dictionary of tracked vehicles.
            yolo_detections: List of YOLO detections (x, y, w, h, class, conf).
        """
        for vehicle_id, vehicle in tracked_vehicles.items():
            if vehicle.bbox is None:
                continue

            best_iou = 0.0
            best_class = None

            for (yx, yy, yw, yh, yclass, yconf) in yolo_detections:
                iou = self._calculate_iou(vehicle.bbox, (yx, yy, yw, yh))
                if iou > best_iou and iou > 0.3:
                    best_iou = iou
                    best_class = yclass

            if best_class is not None:
                vehicle.vehicle_type = best_class

    @staticmethod
    def _calculate_iou(box1, box2):
        """
        Calculate Intersection over Union between two bounding boxes.

        Args:
            box1: (x, y, w, h) first box.
            box2: (x, y, w, h) second box.

        Returns:
            IoU value (0.0 to 1.0).
        """
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        # Convert to (x1, y1, x2, y2) format
        box1_x1, box1_y1 = x1, y1
        box1_x2, box1_y2 = x1 + w1, y1 + h1
        box2_x1, box2_y1 = x2, y2
        box2_x2, box2_y2 = x2 + w2, y2 + h2

        # Intersection
        inter_x1 = max(box1_x1, box2_x1)
        inter_y1 = max(box1_y1, box2_y1)
        inter_x2 = min(box1_x2, box2_x2)
        inter_y2 = min(box1_y2, box2_y2)

        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

        # Union
        box1_area = w1 * h1
        box2_area = w2 * h2
        union_area = box1_area + box2_area - inter_area

        if union_area == 0:
            return 0.0

        return inter_area / union_area

    @staticmethod
    def _draw_legend(frame):
        """Draw a color legend for vehicle types on the frame."""
        legend_x = 10
        legend_y = 60

        for vehicle_type, color in VEHICLE_COLORS.items():
            if vehicle_type == "Unknown":
                continue
            cv2.rectangle(
                frame,
                (legend_x, legend_y),
                (legend_x + 15, legend_y + 15),
                color, -1
            )
            cv2.putText(
                frame, vehicle_type,
                (legend_x + 22, legend_y + 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1,
            )
            legend_y += 22

    def run(self):
        """Run the vehicle speed detection pipeline on the entire video."""
        self.initialize_video()

        print("Processing video... Press 'q' to quit.")

        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            self.frame_count += 1

            # Process the frame
            annotated_frame = self.process_frame(frame)

            # Write to output video
            if self.writer:
                self.writer.write(annotated_frame)

            # Display the frame
            cv2.imshow("Vehicle Speed Detection", annotated_frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cleanup()

    def cleanup(self):
        """Release video resources."""
        print(f"\nProcessing complete. Total frames: {self.frame_count}")

        if self.capture:
            self.capture.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()
