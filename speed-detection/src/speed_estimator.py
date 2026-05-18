"""Speed estimation module for tracked vehicles."""

import math

from src.config import PIXELS_PER_METER, FPS


class SpeedEstimator:
    """Estimates vehicle speed based on pixel displacement across frames."""

    def __init__(self, pixels_per_meter=None, fps=None):
        """
        Initialize the speed estimator.

        Args:
            pixels_per_meter: Calibration factor (pixels per real-world meter).
            fps: Video frames per second.
        """
        self.pixels_per_meter = pixels_per_meter or PIXELS_PER_METER
        self.fps = fps or FPS

    def estimate_speed(self, vehicle):
        """
        Estimate the speed of a tracked vehicle.

        Uses the average displacement over recent frames to smooth
        out noise in the speed calculation.

        Args:
            vehicle: A Vehicle object with position history.

        Returns:
            Estimated speed in km/h.
        """
        positions = vehicle.positions

        if len(positions) < 2:
            return 0.0

        # Use last N positions for smoothing
        num_samples = min(len(positions), 10)
        recent_positions = positions[-num_samples:]

        # Calculate total displacement
        total_displacement = 0.0
        for i in range(1, len(recent_positions)):
            dx = recent_positions[i][0] - recent_positions[i - 1][0]
            dy = recent_positions[i][1] - recent_positions[i - 1][1]
            total_displacement += math.sqrt(dx ** 2 + dy ** 2)

        # Average displacement per frame
        avg_displacement_per_frame = total_displacement / (num_samples - 1)

        # Convert pixels/frame to meters/second
        meters_per_frame = avg_displacement_per_frame / self.pixels_per_meter
        meters_per_second = meters_per_frame * self.fps

        # Convert to km/h
        speed_kmh = meters_per_second * 3.6

        return round(speed_kmh, 1)

    def update_calibration(self, pixels_per_meter):
        """
        Update the calibration factor.

        Args:
            pixels_per_meter: New calibration value.
        """
        self.pixels_per_meter = pixels_per_meter

    def update_fps(self, fps):
        """
        Update the FPS value.

        Args:
            fps: New frames per second value.
        """
        self.fps = fps
