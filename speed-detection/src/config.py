"""Configuration constants for the vehicle speed detection system."""

# Video processing
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Background subtractor parameters
BG_SUBTRACTOR_HISTORY = 500
BG_SUBTRACTOR_THRESHOLD = 50
BG_SUBTRACTOR_DETECT_SHADOWS = True

# Contour filtering
MIN_CONTOUR_WIDTH = 40
MIN_CONTOUR_HEIGHT = 40
MAX_CONTOUR_WIDTH = 500
MAX_CONTOUR_HEIGHT = 500

# Tracking parameters
MAX_DISTANCE_THRESHOLD = 80  # Max pixel distance to associate detections
MAX_FRAMES_TO_SKIP = 10      # Frames before a track is removed

# Speed estimation
PIXELS_PER_METER = 8.0       # Calibration: pixels per real-world meter
FPS = 30                     # Default frames per second

# Detection region of interest (y-coordinates)
ROI_Y_START = 200
ROI_Y_END = 600

# YOLO configuration
YOLO_MODEL_PATH = "models/yolov8n.pt"
YOLO_CONFIDENCE_THRESHOLD = 0.4
VEHICLE_CLASSES = [1, 2, 3, 5, 7]  # bicycle, car, motorcycle, bus, truck

# Visualization - colors per vehicle type (BGR)
VEHICLE_COLORS = {
    "Car": (0, 255, 0),         # Green
    "Motorcycle": (0, 255, 255),  # Yellow
    "Bicycle": (255, 255, 0),   # Cyan
    "Bus": (0, 165, 255),       # Orange
    "Truck": (0, 0, 255),       # Red
    "Unknown": (255, 255, 255), # White
}

BOUNDING_BOX_COLOR = (0, 255, 0)
SPEED_TEXT_COLOR = (0, 0, 255)
FONT_SCALE = 0.6
FONT_THICKNESS = 2
