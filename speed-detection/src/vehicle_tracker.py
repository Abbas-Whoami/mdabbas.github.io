"""Vehicle tracking module using centroid-based tracking."""

import math


class Vehicle:
    """Represents a tracked vehicle with position history."""

    def __init__(self, vehicle_id, centroid):
        """
        Initialize a tracked vehicle.

        Args:
            vehicle_id: Unique identifier for this vehicle.
            centroid: Initial (x, y) position.
        """
        self.vehicle_id = vehicle_id
        self.positions = [centroid]
        self.frames_since_seen = 0
        self.estimated_speed = 0.0
        self.bbox = None
        self.vehicle_type = "Unknown"

    @property
    def last_position(self):
        """Get the most recent position."""
        return self.positions[-1]

    def update(self, centroid, bbox=None):
        """
        Update vehicle position.

        Args:
            centroid: New (x, y) position.
            bbox: Optional bounding box (x, y, w, h).
        """
        self.positions.append(centroid)
        self.frames_since_seen = 0
        self.bbox = bbox

        # Keep only last 30 positions to limit memory
        if len(self.positions) > 30:
            self.positions = self.positions[-30:]


class VehicleTracker:
    """Tracks vehicles across frames using centroid distance matching."""

    def __init__(self, max_distance=80, max_frames_to_skip=10):
        """
        Initialize the tracker.

        Args:
            max_distance: Maximum pixel distance to associate a detection
                          with an existing track.
            max_frames_to_skip: Number of frames a vehicle can be missing
                                before its track is removed.
        """
        self.vehicles = {}
        self.next_vehicle_id = 1
        self.max_distance = max_distance
        self.max_frames_to_skip = max_frames_to_skip

    def update(self, detections):
        """
        Update tracks with new detections.

        Args:
            detections: List of bounding boxes [(x, y, w, h), ...].

        Returns:
            Dictionary of currently tracked vehicles {id: Vehicle}.
        """
        # Calculate centroids for new detections
        centroids = []
        for (x, y, w, h) in detections:
            cx = x + w // 2
            cy = y + h // 2
            centroids.append((cx, cy))

        # If no existing tracks, create new ones for all detections
        if not self.vehicles:
            for i, centroid in enumerate(centroids):
                vehicle = Vehicle(self.next_vehicle_id, centroid)
                vehicle.bbox = detections[i]
                self.vehicles[self.next_vehicle_id] = vehicle
                self.next_vehicle_id += 1
            return self.vehicles

        # Match detections to existing tracks
        matched_detections = set()
        matched_vehicles = set()

        # For each existing vehicle, find the closest detection
        for vehicle_id, vehicle in self.vehicles.items():
            min_distance = float("inf")
            best_match_idx = -1

            for i, centroid in enumerate(centroids):
                if i in matched_detections:
                    continue

                distance = self._calculate_distance(
                    vehicle.last_position, centroid
                )

                if distance < min_distance and distance < self.max_distance:
                    min_distance = distance
                    best_match_idx = i

            if best_match_idx != -1:
                vehicle.update(centroids[best_match_idx],
                               detections[best_match_idx])
                matched_detections.add(best_match_idx)
                matched_vehicles.add(vehicle_id)

        # Increment frames_since_seen for unmatched vehicles
        for vehicle_id in list(self.vehicles.keys()):
            if vehicle_id not in matched_vehicles:
                self.vehicles[vehicle_id].frames_since_seen += 1

        # Remove vehicles that have been missing too long
        vehicles_to_remove = [
            vid for vid, v in self.vehicles.items()
            if v.frames_since_seen > self.max_frames_to_skip
        ]
        for vid in vehicles_to_remove:
            del self.vehicles[vid]

        # Create new tracks for unmatched detections
        for i, centroid in enumerate(centroids):
            if i not in matched_detections:
                vehicle = Vehicle(self.next_vehicle_id, centroid)
                vehicle.bbox = detections[i]
                self.vehicles[self.next_vehicle_id] = vehicle
                self.next_vehicle_id += 1

        return self.vehicles

    @staticmethod
    def _calculate_distance(point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt(
            (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
        )
