# Vehicle Speed Detection System

A computer vision-based vehicle speed detection and classification system using OpenCV, YOLOv8, and background subtraction. This project detects vehicles (cars, bikes, trucks, buses) in video footage, classifies them by type, and estimates their speed.

## Project Structure

```
speed-detection/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point and pipeline orchestration
│   ├── vehicle_detector.py     # Vehicle detection using background subtraction
│   ├── vehicle_classifier.py   # YOLOv8-based vehicle type classification
│   ├── vehicle_tracker.py      # Object tracking and ID assignment
│   ├── speed_estimator.py      # Speed calculation logic
│   └── config.py               # Configuration constants
├── models/
│   └── yolov8n.onnx            # YOLOv8 nano model (download required)
├── input/
│   └── footage.mp4             # Place your video file here
├── output/
│   └── footage_processed.mp4   # Processed output video
├── docs/
│   ├── abstract.md
│   ├── project_report.md
│   └── references.md
├── requirements.txt
├── download_model.py           # Script to download YOLOv8 model
├── run.py                      # Main entry point
└── README.md
```

## Requirements

- Python 3.8+
- OpenCV 4.x
- NumPy
- Ultralytics (for YOLOv8 model export)

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Download and export the YOLOv8 model:
```bash
python download_model.py
```

2. Place your video file as `input/footage.mp4`

3. Run the system:
```bash
python run.py
```

## How It Works

1. **Background Subtraction** - Uses OpenCV's MOG2 to isolate moving objects
2. **Contour Detection** - Identifies vehicle shapes from the foreground mask
3. **YOLO Classification** - YOLOv8 identifies vehicle type (Car, Motorcycle, Truck, Bus, Bicycle)
4. **Object Tracking** - Assigns unique IDs and tracks vehicles across frames
5. **Speed Estimation** - Calculates speed based on pixel displacement and calibration

## Vehicle Types Detected

| Type | Color Code |
|------|-----------|
| Car | Green |
| Motorcycle | Yellow |
| Bicycle | Cyan |
| Bus | Orange |
| Truck | Red |

## License

This project is for educational purposes only.
