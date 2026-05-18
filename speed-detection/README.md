# Vehicle Speed Detection and Classification System

A computer vision-based system that detects vehicles (cars, bikes, trucks, buses) in video footage, classifies them using YOLOv8, tracks them across frames, and estimates their speed in real-time.

## Project Structure

```
speed-detection/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Pipeline orchestration and visualization
│   ├── vehicle_detector.py     # Vehicle detection using background subtraction (MOG2)
│   ├── vehicle_classifier.py   # YOLOv8-based vehicle type classification
│   ├── vehicle_tracker.py      # Centroid-based object tracking
│   ├── speed_estimator.py      # Speed calculation from pixel displacement
│   └── config.py               # All configuration constants
├── models/
│   └── yolov8n.pt              # YOLOv8 nano model (auto-downloaded)
├── input/
│   └── footage.mp4             # Place your video file here
├── output/
│   └── footage_processed.mp4   # Processed output video
├── docs/
│   ├── abstract.md             # Project abstract
│   ├── project_report.md       # Full project report
│   └── references.md           # Academic references
├── requirements.txt            # Python dependencies
├── download_model.py           # YOLO model download script
├── run.py                      # Main entry point
├── start.bat                   # One-click setup and run (Windows)
└── README.md
```

## Quick Start (Windows)

1. Place your video file as `input/footage.mp4`
2. Double-click `start.bat`

That's it. The batch file automatically:
- Creates a Python virtual environment
- Installs all dependencies
- Downloads the YOLO model
- Runs the detection system
- Saves output to `output/footage_processed.mp4`

## Manual Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLO model
python download_model.py

# Run the system
python run.py
```

## How It Works

1. **Background Subtraction (MOG2)** — Isolates moving objects from static background
2. **Morphological Operations** — Cleans noise from the foreground mask
3. **Contour Detection** — Identifies vehicle boundaries
4. **YOLOv8 Classification** — Identifies vehicle type (Car, Motorcycle, Truck, Bus, Bicycle)
5. **Centroid Tracking** — Assigns persistent IDs and tracks vehicles across frames
6. **Speed Estimation** — Converts pixel displacement to km/h using calibration factor

## Vehicle Types and Color Codes

| Type       | Bounding Box Color |
|------------|-------------------|
| Car        | Green             |
| Motorcycle | Yellow            |
| Bicycle    | Cyan              |
| Bus        | Orange            |
| Truck      | Red               |

## Requirements

- Python 3.8+
- Windows 10/11 (for start.bat)
- Input video in MP4 format

## Configuration

All parameters can be adjusted in `src/config.py`:
- `PIXELS_PER_METER` — Calibration factor for speed accuracy
- `YOLO_CONFIDENCE_THRESHOLD` — Detection sensitivity
- `MIN_CONTOUR_WIDTH/HEIGHT` — Minimum vehicle size filter
- `MAX_DISTANCE_THRESHOLD` — Tracking association distance

## License

This project is for educational purposes only.
