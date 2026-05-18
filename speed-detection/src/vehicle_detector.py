"""Vehicle detection module using background subtraction."""

import cv2
import numpy as np

from src.config import (
    BG_SUBTRACTOR_HISTORY,
    BG_SUBTRACTOR_THRESHOLD,
    BG_SUBTRACTOR_DETECT_SHADOWS,
    MIN_CONTOUR_WIDTH,
    MIN_CONTOUR_HEIGHT,
    MAX_CONTOUR_WIDTH,
    MAX_CONTOUR_HEIGHT,
    ROI_Y_START,
    ROI_Y_END,
)


class VehicleDetector:
    """Detects vehicles in video frames using MOG2 background subtraction."""

    def __init__(self):
        """Initialize the background subtractor and morphological kernels."""
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=BG_SUBTRACTOR_HISTORY,
            varThreshold=BG_SUBTRACTOR_THRESHOLD,
            detectShadows=BG_SUBTRACTOR_DETECT_SHADOWS,
        )
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def detect(self, frame):
        """
        Detect vehicles in a single frame.

        Args:
            frame: BGR image (numpy array).

        Returns:
            List of bounding boxes [(x, y, w, h), ...] for detected vehicles.
        """
        # Apply region of interest
        roi = frame[ROI_Y_START:ROI_Y_END, :]

        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(roi)

        # Remove shadows (shadow pixels have value 127 in MOG2)
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

        # Morphological operations to reduce noise
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, self.kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, self.kernel)
        fg_mask = cv2.dilate(fg_mask, self.kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(
            fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        detections = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Filter by size
            if (MIN_CONTOUR_WIDTH <= w <= MAX_CONTOUR_WIDTH and
                    MIN_CONTOUR_HEIGHT <= h <= MAX_CONTOUR_HEIGHT):
                # Adjust y-coordinate back to full frame
                detections.append((x, y + ROI_Y_START, w, h))

        return detections

    def get_foreground_mask(self, frame):
        """
        Get the foreground mask for visualization/debugging.

        Args:
            frame: BGR image (numpy array).

        Returns:
            Binary foreground mask.
        """
        roi = frame[ROI_Y_START:ROI_Y_END, :]
        fg_mask = self.bg_subtractor.apply(roi)
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, self.kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, self.kernel)
        return fg_mask
