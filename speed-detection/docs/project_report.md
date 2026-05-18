# Vehicle Speed Detection and Classification System Using Computer Vision and Deep Learning

---

## 1. Problem Definition and Description

### 1.1 Problem Definition

Road traffic accidents caused by over-speeding are a major concern in urban and highway environments. Monitoring vehicle speeds is essential for traffic management and enforcement of speed limits. Traditional speed detection systems such as radar guns, LIDAR devices, and inductive loop detectors are expensive to deploy and maintain, require specialized hardware, and have limited coverage.

There is a need for a cost-effective, scalable, and software-based solution that can detect, classify, and estimate the speed of vehicles using standard video surveillance cameras already deployed in many locations.

### 1.2 Problem Description

This project addresses the problem of detecting, classifying, and estimating the speed of moving vehicles (cars, bikes, trucks, buses) from pre-recorded video footage. The system processes an MP4 video file, identifies moving vehicles using background subtraction, classifies them by type using YOLOv8 deep learning, tracks them across consecutive frames, and calculates their estimated speed in kilometers per hour (km/h).

The key challenges include:
- Separating moving vehicles from the static background
- Accurately classifying vehicle types in varying conditions
- Handling noise, shadows, and lighting variations
- Maintaining consistent identity of vehicles across frames
- Accurately converting pixel displacement to real-world speed

### 1.3 Scope

- Process pre-recorded MP4 video files
- Detect moving vehicles using background subtraction (MOG2)
- Classify vehicles into types: Car, Motorcycle, Bicycle, Bus, Truck using YOLOv8
- Track vehicles and assign unique identifiers using centroid-based tracking
- Estimate speed based on pixel displacement and calibration
- Generate annotated output video with color-coded bounding boxes, type labels, and speed overlays
- Proof-of-concept implementation for educational purposes

---

## 2. Software Requirements

### 2.1 Software Requirements

| Requirement | Specification |
|-------------|--------------|
| Programming Language | Python 3.8 or higher |
| Computer Vision Library | OpenCV 4.9.0 |
| Deep Learning Framework | PyTorch 2.x (CPU) |
| Object Detection Model | Ultralytics YOLOv8 nano |
| Numerical Computing | NumPy 1.26.4 |
| Operating System | Windows 10/11 |
| IDE | VS Code, PyCharm, or any Python IDE |
| Video Format | MP4 (H.264 codec) |
| Python Package Manager | pip |
| Virtual Environment | venv (built-in) |

### 2.2 Hardware Requirements

| Requirement | Minimum Specification | Recommended Specification |
|-------------|----------------------|--------------------------|
| Processor | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 |
| RAM | 4 GB | 8 GB |
| Storage | 2 GB free space | 5 GB free space |
| Display | 1280 x 720 resolution | 1920 x 1080 resolution |
| GPU | Not required (CPU inference) | Dedicated GPU (faster YOLO inference) |

### 2.3 Functional Requirements

1. The system shall read an MP4 video file as input.
2. The system shall detect moving vehicles in each frame using background subtraction.
3. The system shall classify detected vehicles by type (Car, Motorcycle, Truck, Bus, Bicycle) using YOLOv8.
4. The system shall track detected vehicles across consecutive frames with unique IDs.
5. The system shall estimate the speed of each tracked vehicle in km/h.
6. The system shall display color-coded bounding boxes based on vehicle type.
7. The system shall display vehicle type and speed labels on each detection.
8. The system shall display a color legend on the output video.
9. The system shall save the annotated output video to the output directory.
10. The system shall provide a one-click batch file for setup and execution.

### 2.4 Non-Functional Requirements

1. The system shall process video at a reasonable frame rate on standard hardware.
2. The system shall be modular and maintainable with clear separation of concerns.
3. The system shall handle videos of varying resolutions.
4. The system shall gracefully handle missing input files with user-friendly error messages.
5. The system shall fall back to size-based classification if the YOLO model is unavailable.
6. The system shall run within an isolated virtual environment to avoid dependency conflicts.

---

## 3. System Analysis

### 3.1 Existing System

Current vehicle speed detection and classification methods include:

| Method | Advantages | Disadvantages |
|--------|-----------|---------------|
| Radar Guns | High accuracy, real-time | Expensive, requires operator, limited range |
| LIDAR | Very accurate, long range | Very expensive, requires training |
| Inductive Loop Detectors | Continuous monitoring | Requires road installation, maintenance costly |
| GPS-based Systems | Accurate for individual vehicles | Requires in-vehicle device, privacy concerns |
| Manual CCTV Monitoring | Uses existing infrastructure | Requires human operators, not scalable |

**Limitations of Existing Systems:**
- High cost of deployment and maintenance
- Require specialized hardware
- Limited scalability
- Cannot leverage existing CCTV infrastructure for automated analysis
- No automatic vehicle type classification

### 3.2 Proposed System

The proposed system uses a combination of traditional computer vision and deep learning to detect, classify, and estimate vehicle speed from standard video footage.

**Advantages of the Proposed System:**
- Low cost — uses standard cameras and open-source software
- No specialized hardware required (runs on CPU)
- Automatic vehicle type classification using YOLOv8
- Color-coded visualization for easy identification
- Scalable — can process multiple video feeds
- Non-intrusive — no road installation needed
- One-click setup — batch file handles all installation and execution
- Isolated environment — virtual environment prevents dependency conflicts

**Key Features:**
1. Background subtraction using MOG2 algorithm for motion detection
2. YOLOv8 nano model for vehicle type classification (Car, Motorcycle, Truck, Bus, Bicycle)
3. Morphological operations for noise reduction
4. Contour-based vehicle boundary detection
5. Centroid-based multi-object tracking with unique IDs
6. Calibration-based speed estimation (pixels to km/h)
7. Color-coded annotated video output with legend
8. Automated setup via Windows batch file

### 3.3 Feasibility Study

| Aspect | Assessment |
|--------|-----------|
| Technical Feasibility | OpenCV provides background subtraction; YOLOv8 provides classification; Python is well-suited for rapid prototyping |
| Economic Feasibility | Uses free, open-source tools (Python, OpenCV, Ultralytics); no hardware cost beyond a standard computer |
| Operational Feasibility | One-click batch file for setup; minimal technical knowledge required to run |
| Schedule Feasibility | Modular design allows parallel development of detection, classification, tracking, and speed modules |

---

## 4. Data Flow Diagram

### 4.1 Context Diagram (Level 0)

```
+------------------+          +---------------------------+          +------------------+
|                  |  Video   |                           |  Output  |                  |
|   Video Input    |--------->|  Vehicle Speed Detection  |--------->|  Annotated Video |
|  (footage.mp4)  |          |  & Classification System  |          |  + Speed Data    |
|                  |          |                           |          |  + Vehicle Types |
+------------------+          +---------------------------+          +------------------+
```

### 4.2 Level 1 DFD

```
                    +-------------------+
                    |   Video Input     |
                    | (footage.mp4)     |
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
                    |     (MOG2)        |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 3.0 Vehicle       |
                    |     Detection     |
                    |   (Contours)      |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 4.0 Vehicle       |
                    |   Classification  |
                    |    (YOLOv8)       |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 5.0 Vehicle       |
                    |     Tracking      |
                    |   (Centroid)      |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 6.0 Speed         |
                    |     Estimation    |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    | 7.0 Output        |
                    |     Generation    |
                    | (Annotated Video) |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    | Output Video      |
                    | (footage_         |
                    |  processed.mp4)   |
                    +-------------------+
```

### 4.3 Level 2 DFD — Vehicle Detection (Process 3.0)

```
+------------------+     +-------------------+     +------------------+
| Foreground Mask  |---->| Morphological     |---->| Contour          |
| (from MOG2)     |     | Operations        |     | Detection        |
+------------------+     | (Close, Open,     |     +--------+---------+
                         |  Dilate)          |              |
                         +-------------------+              v
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

### 4.4 Level 2 DFD — Vehicle Classification (Process 4.0)

```
+------------------+     +-------------------+     +------------------+
| Video Frame      |---->| YOLOv8 Inference  |---->| NMS Filtering    |
|                  |     | (every 5 frames)  |     | (Remove overlaps)|
+------------------+     +-------------------+     +--------+---------+
                                                            |
                                                            v
                                                   +--------+---------+
                                                   | IoU Matching     |
                                                   | (Match to tracks)|
                                                   +--------+---------+
                                                            |
                                                            v
                                                   +------------------+
                                                   | Vehicle Type     |
                                                   | Assignment       |
                                                   +------------------+
```

---

## 5. System Design

### 5.1 Architectural Design

The system follows a **pipeline architecture** with a hybrid detection approach combining traditional computer vision and deep learning:

```
┌─────────────────────────────────────────────────────────────────────┐
│            Vehicle Speed Detection & Classification System            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────┐   ┌──────────────┐   ┌───────────────┐   ┌─────────┐ │
│  │  Video   │──>│   Vehicle    │──>│   Vehicle     │──>│ Vehicle │ │
│  │  Input   │   │  Detector    │   │   Tracker     │   │ Speed   │ │
│  └──────────┘   │  (MOG2)      │   │  (Centroid)   │   │ Est.    │ │
│       │         └──────────────┘   └───────────────┘   └─────────┘ │
│       │                                    ^                   │     │
│       │         ┌──────────────┐           │                   │     │
│       │────────>│   Vehicle    │───────────┘                   │     │
│       │         │  Classifier  │                               │     │
│       │         │  (YOLOv8)    │                               │     │
│       │         └──────────────┘                               │     │
│       │                                                        │     │
│       │              ┌──────────────────┐                      │     │
│       └─────────────>│   Main System    │<─────────────────────┘     │
│                      │  (Orchestrator)  │                            │
│                      └────────┬─────────┘                            │
│                               │                                       │
│                      ┌────────┴─────────┐                            │
│                      │  Video Output    │                            │
│                      │  (Annotated)     │                            │
│                      └──────────────────┘                            │
├─────────────────────────────────────────────────────────────────────┤
│                      config.py (Parameters)                          │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Module Design

| Module | Class | Responsibility |
|--------|-------|---------------|
| `vehicle_detector.py` | `VehicleDetector` | MOG2 background subtraction, morphological ops, contour detection |
| `vehicle_classifier.py` | `VehicleClassifier` | YOLOv8 inference, vehicle type identification, fallback classification |
| `vehicle_tracker.py` | `VehicleTracker`, `Vehicle` | Multi-object tracking, ID assignment, position history |
| `speed_estimator.py` | `SpeedEstimator` | Pixel displacement to km/h conversion |
| `main.py` | `VehicleSpeedDetectionSystem` | Pipeline orchestration, IoU matching, visualization, video I/O |
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
│       VehicleClassifier         │
├─────────────────────────────────┤
│ - model_path: str               │
│ - model: YOLO                   │
│ - VEHICLE_CLASS_MAP: dict       │
├─────────────────────────────────┤
│ + detect_and_classify(frame)    │
│ + classify_by_bbox(frame, bbox) │
│ - _load_model()                 │
│ - _fallback_classify(bbox)      │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│         Vehicle                 │
├─────────────────────────────────┤
│ - vehicle_id: int               │
│ - positions: list               │
│ - frames_since_seen: int        │
│ - estimated_speed: float        │
│ - bbox: tuple                   │
│ - vehicle_type: str             │
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
│ - classifier: VehicleClassifier │
│ - tracker: VehicleTracker       │
│ - speed_estimator: SpeedEstimator│
│ - capture: VideoCapture         │
│ - writer: VideoWriter           │
│ - frame_count: int              │
├─────────────────────────────────┤
│ + initialize_video()            │
│ + process_frame(frame)          │
│ + run()                         │
│ + cleanup()                     │
│ - _match_classifications()      │
│ - _calculate_iou(box1, box2)    │
│ - _draw_legend(frame)           │
└─────────────────────────────────┘
```

---

## 6. Database Design

This project does not use a traditional database. All data is processed in-memory during video analysis. The following data structures serve as the runtime data store:

### 6.1 In-Memory Data Structures

**Vehicle Record:**

| Field | Type | Description |
|-------|------|-------------|
| vehicle_id | Integer | Unique identifier for the tracked vehicle |
| positions | List of tuples | History of (x, y) centroid positions |
| frames_since_seen | Integer | Counter for frames since last detection |
| estimated_speed | Float | Current estimated speed in km/h |
| bbox | Tuple (x, y, w, h) | Current bounding box coordinates |
| vehicle_type | String | Classification: Car, Motorcycle, Truck, Bus, Bicycle |

**Detection Record (Background Subtraction):**

| Field | Type | Description |
|-------|------|-------------|
| x | Integer | Top-left x coordinate of bounding box |
| y | Integer | Top-left y coordinate of bounding box |
| w | Integer | Width of bounding box |
| h | Integer | Height of bounding box |

**YOLO Detection Record:**

| Field | Type | Description |
|-------|------|-------------|
| x | Integer | Top-left x coordinate |
| y | Integer | Top-left y coordinate |
| w | Integer | Width of bounding box |
| h | Integer | Height of bounding box |
| class_name | String | Vehicle type (Car, Motorcycle, etc.) |
| confidence | Float | Detection confidence (0.0 to 1.0) |

### 6.2 Configuration Data Store (`config.py`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| PIXELS_PER_METER | Float | 8.0 | Calibration factor |
| FPS | Integer | 30 | Video frame rate |
| YOLO_CONFIDENCE_THRESHOLD | Float | 0.4 | Minimum detection confidence |
| MAX_DISTANCE_THRESHOLD | Integer | 80 | Tracking association distance |
| MAX_FRAMES_TO_SKIP | Integer | 10 | Frames before track removal |

### 6.3 Data Flow

```
Frame (numpy array)
    → Foreground Mask (binary image)
    → Contours (list)
    → Bounding Boxes (list of tuples)
    → YOLO Classifications (list of tuples with class names)
    → Vehicle Objects (dict with type, speed, positions)
    → Annotated Frame (numpy array with overlays)
    → Output Video File
```

---

## 7. Implementation

### 7.1 Modules of the Work

#### Module 1: Vehicle Detection (`vehicle_detector.py`)

**Purpose:** Detect moving vehicles in each video frame using background subtraction.

**Algorithm:**
1. Extract the Region of Interest (ROI) from the frame (y: 200 to 600)
2. Apply MOG2 background subtraction to generate foreground mask
3. Threshold the mask to remove shadow pixels (value > 200)
4. Apply morphological closing to fill gaps in vehicle shapes
5. Apply morphological opening to remove small noise
6. Dilate the mask to merge nearby regions (2 iterations)
7. Find external contours in the processed mask
8. Filter contours by minimum (40px) and maximum (500px) size thresholds
9. Return list of bounding boxes for valid detections

**Key Parameters:**
- `BG_SUBTRACTOR_HISTORY = 500` — Number of frames for background model learning
- `BG_SUBTRACTOR_THRESHOLD = 50` — Variance threshold for pixel classification
- `MIN_CONTOUR_WIDTH = 40` — Minimum vehicle width in pixels
- `MIN_CONTOUR_HEIGHT = 40` — Minimum vehicle height in pixels

#### Module 2: Vehicle Classification (`vehicle_classifier.py`)

**Purpose:** Classify detected vehicles by type using YOLOv8 deep learning model.

**Algorithm:**
1. Load YOLOv8 nano model (.pt format) using Ultralytics library
2. Run inference on the full frame (every 5 frames for performance)
3. Filter detections to vehicle classes only (COCO IDs: 1, 2, 3, 5, 7)
4. Apply confidence threshold (0.4) to remove weak detections
5. Match YOLO detections to tracked vehicles using IoU (Intersection over Union)
6. Assign vehicle type to matched tracks
7. Fall back to size-based heuristic if YOLO model is unavailable

**COCO Vehicle Classes:**
| Class ID | Vehicle Type |
|----------|-------------|
| 1 | Bicycle |
| 2 | Car |
| 3 | Motorcycle |
| 5 | Bus |
| 7 | Truck |

**Fallback Classification (size-based):**
- Area < 3000px² → Motorcycle
- Area < 8000px² → Motorcycle or Car (based on aspect ratio)
- Area < 25000px² → Car
- Area < 50000px² → Bus or Truck (based on aspect ratio)
- Area ≥ 50000px² → Truck

#### Module 3: Vehicle Tracking (`vehicle_tracker.py`)

**Purpose:** Maintain consistent identity of vehicles across frames.

**Algorithm:**
1. Calculate centroids for all new detections
2. For each existing tracked vehicle, find the closest new detection
3. If Euclidean distance is below threshold (80px), update the vehicle's position
4. Increment "frames since seen" counter for unmatched vehicles
5. Remove vehicles that have been missing for more than 10 frames
6. Create new vehicle tracks for unmatched detections
7. Maintain position history (last 30 positions) for speed calculation

**Key Parameters:**
- `MAX_DISTANCE_THRESHOLD = 80` — Maximum pixel distance for matching
- `MAX_FRAMES_TO_SKIP = 10` — Frames before removing a lost track

#### Module 4: Speed Estimation (`speed_estimator.py`)

**Purpose:** Convert pixel displacement to real-world speed in km/h.

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

#### Module 5: Main System (`main.py`)

**Purpose:** Orchestrate the entire pipeline, handle video I/O, and generate annotated output.

**Responsibilities:**
- Open and validate the input video file
- Read frames sequentially from the video
- Pass frames through detection → classification → tracking → speed estimation
- Match YOLO classifications to tracked vehicles using IoU overlap (threshold: 0.3)
- Annotate frames with color-coded bounding boxes per vehicle type
- Draw vehicle type labels, speed values, and tracking IDs
- Draw color legend and frame statistics
- Write annotated frames to output video
- Display real-time preview window (press 'Q' to quit)
- Handle cleanup on completion or user interrupt

#### Module 6: Configuration (`config.py`)

**Purpose:** Centralize all tunable parameters for easy adjustment.

**Categories:**
- Video processing parameters (resolution, ROI)
- Background subtractor parameters (history, threshold, shadows)
- Contour filtering thresholds (min/max size)
- YOLO configuration (model path, confidence threshold)
- Tracking parameters (distance threshold, frame skip limit)
- Speed estimation calibration (pixels per meter, FPS)
- Visualization settings (colors per vehicle type, font settings)

#### Module 7: Setup Automation (`start.bat`)

**Purpose:** Provide one-click setup and execution for non-technical users.

**Steps performed:**
1. Check Python installation
2. Verify input video file exists
3. Create Python virtual environment
4. Activate virtual environment
5. Install all dependencies from requirements.txt
6. Download YOLO model if not present
7. Create output directory
8. Run the detection system
9. Display completion message

---

## 8. Result and Discussion

### 8.1 Results

The system successfully demonstrates:

1. **Vehicle Detection:** Moving vehicles are detected using MOG2 background subtraction. The algorithm effectively separates foreground objects from the static background after an initial learning period of approximately 50-100 frames.

2. **Vehicle Classification:** YOLOv8 nano model accurately classifies vehicles into five categories (Car, Motorcycle, Bicycle, Bus, Truck). The model runs every 5 frames to balance accuracy with performance. Classification results are cached on tracked vehicles for smooth labeling.

3. **Color-Coded Visualization:** Each vehicle type is displayed with a distinct bounding box color:
   - Car → Green
   - Motorcycle → Yellow
   - Bicycle → Cyan
   - Bus → Orange
   - Truck → Red

4. **Vehicle Tracking:** Detected vehicles are assigned unique IDs and tracked across frames. The centroid-based approach works well for vehicles moving at moderate speeds with minimal occlusion.

5. **Speed Estimation:** Speed values are calculated and displayed in real-time. The accuracy depends on the calibration factor (pixels_per_meter) which must be set based on known distances in the video scene.

6. **Output Generation:** An annotated video is produced with:
   - Color-coded bounding boxes per vehicle type
   - Vehicle type and speed labels with background for readability
   - Vehicle tracking IDs
   - Frame counter and vehicle count overlay
   - Color legend showing type-to-color mapping
   - Blue ROI boundary lines

### 8.2 Discussion

**Strengths:**
- Hybrid approach combines fast background subtraction with accurate deep learning classification
- YOLOv8 nano is lightweight (~6MB) and runs on CPU without GPU requirement
- Color-coded output makes it easy to visually identify vehicle types
- Modular design allows easy modification of individual components
- Fallback classification ensures the system works even without the YOLO model
- One-click batch file makes it accessible to non-technical users
- Virtual environment isolates dependencies from the system Python

**Limitations:**
- Speed accuracy depends heavily on camera calibration (pixels_per_meter)
- Background subtraction requires a static camera
- Initial frames produce no detections (background model learning phase)
- Occlusion between vehicles can cause tracking errors or ID switches
- YOLO runs every 5 frames — fast-moving vehicles may briefly show incorrect type
- Performance on CPU is adequate but not real-time for high-resolution video
- Perspective distortion is not corrected

**Accuracy Considerations:**
- The pixels_per_meter calibration is the most critical factor for speed accuracy
- Camera angle affects the apparent speed of vehicles
- YOLOv8 nano achieves ~37% mAP on COCO — sufficient for vehicle classification
- Speed values should be treated as estimates, not precise measurements
- IoU threshold of 0.3 for matching provides good balance between precision and recall

---

## 9. Conclusion

This project successfully implements a proof-of-concept vehicle speed detection and classification system combining traditional computer vision with modern deep learning. The system demonstrates that it is feasible to detect, classify, and estimate vehicle speeds from standard video footage using open-source tools without requiring expensive specialized hardware.

The key contributions of this project are:

1. **Hybrid Detection Pipeline:** Combining MOG2 background subtraction (fast, lightweight) with YOLOv8 (accurate classification) provides the best of both approaches.

2. **Vehicle Type Classification:** Integration of YOLOv8 nano model enables automatic identification of five vehicle types with color-coded visualization.

3. **Complete Tracking System:** Centroid-based tracking maintains vehicle identities across frames, enabling continuous speed monitoring.

4. **User-Friendly Deployment:** The Windows batch file (`start.bat`) enables one-click setup and execution, making the system accessible to users without technical knowledge.

5. **Modular Architecture:** Clear separation of concerns allows individual components to be upgraded independently (e.g., replacing centroid tracking with DeepSORT, or upgrading to YOLOv8 medium model).

While the system has limitations in terms of speed accuracy and robustness compared to commercial solutions, it serves as an effective educational demonstration of computer vision and deep learning principles applied to traffic monitoring.

---

## 10. References

1. Zivkovic, Z. (2004). "Improved Adaptive Gaussian Mixture Model for Background Subtraction." *Proceedings of the 17th International Conference on Pattern Recognition (ICPR)*, IEEE.

2. Zivkovic, Z., & van der Heijden, F. (2006). "Efficient Adaptive Density Estimation per Image Pixel for the Task of Background Subtraction." *Pattern Recognition Letters*, 27(7), 773-780.

3. Jocher, G., Chaurasia, A., & Qiu, J. (2023). "Ultralytics YOLOv8." Available at: https://github.com/ultralytics/ultralytics

4. Redmon, J., et al. (2016). "You Only Look Once: Unified, Real-Time Object Detection." *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.

5. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media.

6. OpenCV Documentation. "Background Subtraction." Available at: https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html

7. Lin, T. Y., et al. (2014). "Microsoft COCO: Common Objects in Context." *European Conference on Computer Vision (ECCV)*, Springer.

8. Seenouvong, N., et al. (2016). "A Computer Vision Based Vehicle Speed Measurement System." *International Conference on Information Technology and Electrical Engineering (ICITEE)*, IEEE.

9. Luvizon, D. C., Nassu, B. T., & Minetto, R. (2017). "A Video-Based System for Vehicle Speed Measurement in Urban Roadways." *IEEE Transactions on Intelligent Transportation Systems*, 18(6), 1393-1404.

10. Ultralytics Documentation. "YOLOv8." Available at: https://docs.ultralytics.com/

11. NumPy Documentation. Available at: https://numpy.org/doc/

12. Python Software Foundation. "Python 3 Documentation." Available at: https://docs.python.org/3/
