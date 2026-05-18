# Vehicle Speed Detection System Using Computer Vision

---

## 1. Problem Definition and Description

### 1.1 Problem Definition

Road traffic accidents caused by over-speeding are a major concern in urban and highway environments. Monitoring vehicle speeds is essential for traffic management and enforcement of speed limits. Traditional speed detection systems such as radar guns, LIDAR devices, and inductive loop detectors are expensive to deploy and maintain, require specialized hardware, and have limited coverage.

There is a need for a cost-effective, scalable, and software-based solution that can estimate vehicle speeds using standard video surveillance cameras already deployed in many locations.

### 1.2 Problem Description

This project addresses the problem of detecting and estimating the speed of moving vehicles (cars, bikes, and other motorized vehicles) from pre-recorded video footage. The system processes an MP4 video file, identifies moving vehicles using computer vision techniques, tracks them across consecutive frames, and calculates their estimated speed in kilometers per hour (km/h).

The key challenges include:
- Separating moving vehicles from the static background
- Handling noise, shadows, and lighting variations
- Maintaining consistent identity of vehicles across frames
- Accurately converting pixel displacement to real-world speed

### 1.3 Scope

- Process pre-recorded MP4 video files
- Detect cars, bikes, and other vehicles
- Track vehicles and assign unique identifiers
- Estimate speed based on pixel displacement and calibration
- Generate annotated output video with speed overlays
- Proof-of-concept implementation for educational purposes

---

## 2. Software Requirements

### 2.1 Software Requirements

| Requirement | Specification |
|-------------|--------------|
| Programming Language | Python 3.8 or higher |
| Computer Vision Library | OpenCV 4.9.0 |
| Numerical Computing | NumPy 1.26.4 |
| Operating System | Windows 10/11, Linux, or macOS |
| IDE | VS Code, PyCharm, or any Python IDE |
| Video Format | MP4 (H.264 codec) |
| Python Package Manager | pip |

### 2.2 Hardware Requirements

| Requirement | Minimum Specification | Recommended Specification |
|-------------|----------------------|--------------------------|
| Processor | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB free space | 2 GB free space |
| Display | 1280 x 720 resolution | 1920 x 1080 resolution |
| GPU | Not required | Dedicated GPU (for faster processing) |

### 2.3 Functional Requirements

1. The system shall read an MP4 video file as input.
2. The system shall detect moving vehicles in each frame.
3. The system shall track detected vehicles across consecutive frames.
4. The system shall estimate the speed of each tracked vehicle.
5. The system shall display bounding boxes around detected vehicles.
6. The system shall display speed labels for each vehicle.
7. The system shall save the annotated output video.

### 2.4 Non-Functional Requirements

1. The system shall process video at a reasonable frame rate.
2. The system shall be modular and maintainable.
3. The system shall handle videos of varying resolutions.
4. The system shall gracefully handle missing input files.

---

## 3. System Analysis

### 3.1 Existing System

Current vehicle speed detection methods include:

| Method | Advantages | Disadvantages |
|--------|-----------|---------------|
| Radar Guns | High accuracy, real-time | Expensive, requires operator, limited range |
| LIDAR | Very accurate, long range | Very expensive, requires training |
| Inductive Loop Detectors | Continuous monitoring | Requires road installation, maintenance costly |
| GPS-based Systems | Accurate for individual vehicles | Requires in-vehicle device, privacy concerns |

**Limitations of Existing Systems:**
- High cost of deployment and maintenance
- Require specialized hardware
- Limited scalability
- Cannot leverage existing CCTV infrastructure

### 3.2 Proposed System

The proposed system uses computer vision techniques to estimate vehicle speed from standard video footage. It leverages existing camera infrastructure and requires only a computer with Python installed.

**Advantages of the Proposed System:**
- Low cost — uses standard cameras and open-source software
- No specialized hardware required
- Scalable — can process multiple video feeds
- Non-intrusive — no road installation needed
- Flexible — configurable parameters for different scenarios

**Key Features:**
1. Background subtraction using MOG2 algorithm
2. Morphological operations for noise reduction
3. Contour-based vehicle detection
4. Centroid-based multi-object tracking
5. Calibration-based speed estimation
6. Annotated video output with speed overlays

### 3.3 Feasibility Study

| Aspect | Assessment |
|--------|-----------|
| Technical Feasibility | OpenCV provides all required algorithms; Python is well-suited for rapid prototyping |
| Economic Feasibility | Uses free, open-source tools; no hardware cost beyond a standard computer |
| Operational Feasibility | Simple command-line interface; minimal training required |

---

## 4. Data Flow Diagram

### 4.1 Context Diagram (Level 0)

```
+------------------+          +---------------------------+          +------------------+
|                  |  Video   |                           |  Output  |                  |
|   Video Input    |--------->|  Vehicle Speed Detection  |--------->|  Annotated Video |
|   (footage.mp4) |          |        System             |          |  + Speed Data    |
|                  |          |                           |          |                  |
+------------------+          +---------------------------+          +------------------+
```

### 4.2 Level 1 DFD

```
                    +-------------------+
                    |   Video Input     |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 1.0 Frame         |
                    |     Extraction    |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 2.0 Background    |
                    |     Subtraction   |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 3.0 Vehicle       |
                    |     Detection     |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 4.0 Vehicle       |
                    |     Tracking      |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 5.0 Speed         |
                    |     Estimation    |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 6.0 Output        |
                    |     Generation    |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    | Annotated Video   |
                    +-------------------+
```

### 4.3 Level 2 DFD — Vehicle Detection (Process 3.0)

```
+------------------+     +-------------------+     +------------------+
| Foreground Mask  |---->| Morphological     |---->| Contour          |
| (from MOG2)     |     | Operations        |     | Detection        |
+------------------+     +-------------------+     +--------+---------+
                                                            |
                                                            v
                                                   +--------+---------+
                                                   | Size Filtering   |
                                                   | (min/max bounds) |
                                                   +--------+---------+
                                                            |
                                                            v
                                                   +------------------+
                                                   | Bounding Boxes   |
                                                   +------------------+
```

---

## 5. System Design

### 5.1 Architectural Design

The system follows a **pipeline architecture** where data flows sequentially through processing stages:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Vehicle Speed Detection System                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐   ┌──────────────┐   ┌─────────────┐   ┌───────┐ │
│  │  Video   │──>│   Vehicle    │──>│   Vehicle   │──>│ Speed │ │
│  │  Input   │   │  Detector    │   │   Tracker   │   │ Est.  │ │
│  └──────────┘   └──────────────┘   └─────────────┘   └───────┘ │
│       │                                                    │     │
│       │              ┌──────────────┐                      │     │
│       └─────────────>│  Main System │<─────────────────────┘     │
│                      │ (Orchestrator)│                            │
│                      └──────┬───────┘                            │
│                             │                                     │
│                      ┌──────┴───────┐                            │
│                      │ Video Output │                            │
│                      └──────────────┘                            │
├─────────────────────────────────────────────────────────────────┤
│                      config.py (Parameters)                      │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Module Design

| Module | Class | Responsibility |
|--------|-------|---------------|
| `vehicle_detector.py` | `VehicleDetector` | Background subtraction, morphological ops, contour detection |
| `vehicle_tracker.py` | `VehicleTracker`, `Vehicle` | Multi-object tracking, ID assignment |
| `speed_estimator.py` | `SpeedEstimator` | Pixel-to-speed conversion |
| `main.py` | `VehicleSpeedDetectionSystem` | Pipeline orchestration, visualization |
| `config.py` | — | Centralized configuration constants |

### 5.3 Class Design

```
┌─────────────────────────────────┐
│       VehicleDetector           │
├─────────────────────────────────┤
│ - bg_subtractor: MOG2           │
│ - kernel: MorphElement          │
├─────────────────────────────────┤
│ + detect(frame) -> list         │
│ + get_foreground_mask(frame)    │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│         Vehicle                 │
├─────────────────────────────────┤
│ - vehicle_id: int               │
│ - positions: list               │
│ - frames_since_seen: int        │
│ - estimated_speed: float        │
│ - bbox: tuple                   │
├─────────────────────────────────┤
│ + last_position -> tuple        │
│ + update(centroid, bbox)        │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       VehicleTracker            │
├─────────────────────────────────┤
│ - vehicles: dict                │
│ - next_vehicle_id: int          │
│ - max_distance: int             │
│ - max_frames_to_skip: int       │
├─────────────────────────────────┤
│ + update(detections) -> dict    │
│ - _calculate_distance(p1, p2)   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       SpeedEstimator            │
├─────────────────────────────────┤
│ - pixels_per_meter: float       │
│ - fps: int                      │
├─────────────────────────────────┤
│ + estimate_speed(vehicle)       │
│ + update_calibration(ppm)       │
│ + update_fps(fps)               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  VehicleSpeedDetectionSystem    │
├─────────────────────────────────┤
│ - video_path: str               │
│ - output_path: str              │
│ - detector: VehicleDetector     │
│ - tracker: VehicleTracker       │
│ - speed_estimator: SpeedEstimator│
│ - capture: VideoCapture         │
│ - writer: VideoWriter           │
├─────────────────────────────────┤
│ + initialize_video()            │
│ + process_frame(frame)          │
│ + run()                         │
│ + cleanup()                     │
└─────────────────────────────────┘
```

---

## 6. Database Design

This project does not use a traditional database. All data is processed in-memory during video analysis. However, the following data structures serve as the runtime data store:

### 6.1 In-Memory Data Structures

**Vehicle Record:**

| Field | Type | Description |
|-------|------|-------------|
| vehicle_id | Integer | Unique identifier for the tracked vehicle |
| positions | List of tuples | History of (x, y) centroid positions |
| frames_since_seen | Integer | Counter for frames since last detection |
| estimated_speed | Float | Current estimated speed in km/h |
| bbox | Tuple (x, y, w, h) | Current bounding box coordinates |

**Detection Record:**

| Field | Type | Description |
|-------|------|-------------|
| x | Integer | Top-left x coordinate of bounding box |
| y | Integer | Top-left y coordinate of bounding box |
| w | Integer | Width of bounding box |
| h | Integer | Height of bounding box |

### 6.2 Data Flow

```
Frame (numpy array) → Foreground Mask (binary image) → Contours (list)
    → Bounding Boxes (list of tuples) → Vehicle Objects (dict)
    → Speed Values (float) → Annotated Frame (numpy array)
```

---

## 7. Implementation

### 7.1 Modules of the Work

#### Module 1: Vehicle Detection (`vehicle_detector.py`)

**Purpose:** Detect moving vehicles in each video frame.

**Algorithm:**
1. Extract the Region of Interest (ROI) from the frame
2. Apply MOG2 background subtraction to generate foreground mask
3. Threshold the mask to remove shadow pixels
4. Apply morphological closing to fill gaps in vehicle shapes
5. Apply morphological opening to remove small noise
6. Dilate the mask to merge nearby regions
7. Find external contours in the processed mask
8. Filter contours by minimum and maximum size thresholds
9. Return list of bounding boxes for valid detections

**Key Parameters:**
- `BG_SUBTRACTOR_HISTORY = 500` — Number of frames for background model
- `BG_SUBTRACTOR_THRESHOLD = 50` — Variance threshold for pixel classification
- `MIN_CONTOUR_WIDTH = 40` — Minimum vehicle width in pixels
- `MIN_CONTOUR_HEIGHT = 40` — Minimum vehicle height in pixels

#### Module 2: Vehicle Tracking (`vehicle_tracker.py`)

**Purpose:** Maintain consistent identity of vehicles across frames.

**Algorithm:**
1. Calculate centroids for all new detections
2. For each existing tracked vehicle, find the closest new detection
3. If distance is below threshold, update the vehicle's position
4. Increment "frames since seen" counter for unmatched vehicles
5. Remove vehicles that have been missing for too many frames
6. Create new vehicle tracks for unmatched detections

**Key Parameters:**
- `MAX_DISTANCE_THRESHOLD = 80` — Maximum pixel distance for matching
- `MAX_FRAMES_TO_SKIP = 10` — Frames before removing a lost track

#### Module 3: Speed Estimation (`speed_estimator.py`)

**Purpose:** Convert pixel displacement to real-world speed.

**Algorithm:**
1. Get the last N positions of the vehicle (N = 10 for smoothing)
2. Calculate total Euclidean displacement across these positions
3. Compute average displacement per frame
4. Convert pixels/frame to meters/second using calibration factor
5. Convert meters/second to km/h (multiply by 3.6)

**Formula:**
```
speed (km/h) = (avg_pixel_displacement / pixels_per_meter) × fps × 3.6
```

#### Module 4: Main System (`main.py`)

**Purpose:** Orchestrate the entire pipeline and handle video I/O.

**Responsibilities:**
- Open and validate the input video file
- Read frames sequentially
- Pass frames through detection → tracking → speed estimation
- Annotate frames with bounding boxes and speed labels
- Write annotated frames to output video
- Display real-time preview window
- Handle cleanup on completion or user interrupt

#### Module 5: Configuration (`config.py`)

**Purpose:** Centralize all tunable parameters.

**Categories:**
- Video processing parameters
- Background subtractor parameters
- Contour filtering thresholds
- Tracking parameters
- Speed estimation calibration
- Visualization settings

---

## 8. Result and Discussion

### 8.1 Results

The system successfully demonstrates:

1. **Vehicle Detection:** Moving vehicles are detected using background subtraction. The MOG2 algorithm effectively separates foreground objects from the static background after an initial learning period of approximately 50-100 frames.

2. **Vehicle Tracking:** Detected vehicles are assigned unique IDs and tracked across frames. The centroid-based approach works well for vehicles moving at moderate speeds with minimal occlusion.

3. **Speed Estimation:** Speed values are calculated and displayed in real-time. The accuracy depends on the calibration factor (pixels_per_meter) which must be set based on known distances in the video scene.

4. **Output Generation:** An annotated video is produced with:
   - Green bounding boxes around detected vehicles
   - Vehicle ID and estimated speed labels
   - Frame counter and vehicle count overlay
   - Blue ROI boundary lines

### 8.2 Discussion

**Strengths:**
- Simple and lightweight — runs on standard hardware without GPU
- Modular design allows easy modification of individual components
- Configurable parameters adapt to different video scenarios
- Real-time visualization aids in debugging and calibration

**Limitations:**
- Speed accuracy depends heavily on camera calibration
- Background subtraction requires a static camera
- Initial frames produce no detections (background model learning phase)
- Occlusion between vehicles can cause tracking errors
- No vehicle classification (cannot distinguish car from bike)
- Performance degrades in poor lighting or adverse weather

**Accuracy Considerations:**
- The pixels_per_meter calibration is the most critical factor
- Camera angle affects the apparent speed of vehicles
- Perspective distortion is not corrected in this implementation
- Speed values should be treated as estimates, not precise measurements

---

## 9. Conclusion

This project successfully implements a proof-of-concept vehicle speed detection system using computer vision techniques. The system demonstrates that it is feasible to estimate vehicle speeds from standard video footage using open-source tools (Python and OpenCV) without requiring expensive specialized hardware.

The key contributions of this project are:
1. Implementation of a complete detection-tracking-estimation pipeline
2. Use of MOG2 background subtraction for robust vehicle detection
3. Centroid-based tracking for maintaining vehicle identities
4. Configurable calibration system for speed estimation

While the system has limitations in terms of accuracy and robustness compared to commercial solutions, it serves as an effective educational demonstration of computer vision principles applied to traffic monitoring. The modular architecture allows for future enhancements such as deep learning-based detection, Kalman filter tracking, and perspective correction.

---

## 10. References

1. Zivkovic, Z. (2004). "Improved Adaptive Gaussian Mixture Model for Background Subtraction." *Proceedings of the 17th International Conference on Pattern Recognition (ICPR)*, IEEE.

2. Zivkovic, Z., & van der Heijden, F. (2006). "Efficient Adaptive Density Estimation per Image Pixel for the Task of Background Subtraction." *Pattern Recognition Letters*, 27(7), 773-780.

3. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media.

4. OpenCV Documentation. "Background Subtraction." Available at: https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html

5. OpenCV Documentation. "Contour Features." Available at: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html

6. Seenouvong, N., et al. (2016). "A Computer Vision Based Vehicle Speed Measurement System." *International Conference on Information Technology and Electrical Engineering (ICITEE)*, IEEE.

7. Dogan, S., Temiz, M. S., & Kulur, S. (2010). "Real-Time Speed Estimation of Moving Vehicles from Side View Images from an Uncalibrated Video Camera." *Sensors*, 10(5), 4805-4824.

8. Luvizon, D. C., Nassu, B. T., & Minetto, R. (2017). "A Video-Based System for Vehicle Speed Measurement in Urban Roadways." *IEEE Transactions on Intelligent Transportation Systems*, 18(6), 1393-1404.

9. NumPy Documentation. Available at: https://numpy.org/doc/

10. Python Software Foundation. "Python 3 Documentation." Available at: https://docs.python.org/3/
