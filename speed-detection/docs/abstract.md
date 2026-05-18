# Abstract

## Vehicle Speed Detection and Classification System Using Computer Vision and Deep Learning

### Problem Statement

Traffic monitoring and speed enforcement are critical for road safety. Traditional speed detection methods rely on expensive hardware such as radar guns, LIDAR, and inductive loop detectors. This project proposes a cost-effective, software-based approach to vehicle speed estimation and classification using computer vision and deep learning techniques applied to standard video footage.

### Objective

To design and implement a vehicle speed detection and classification system that can:

1. Detect moving vehicles (cars, bikes, trucks, buses) in video footage using background subtraction.
2. Classify detected vehicles by type using YOLOv8 deep learning model.
3. Track detected vehicles across consecutive video frames using centroid-based tracking.
4. Estimate the speed of each tracked vehicle in real-time.
5. Generate annotated output video with color-coded bounding boxes, vehicle type labels, and speed overlays.

### Methodology

The system employs the following techniques:

- **Background Subtraction (MOG2):** Gaussian Mixture Model-based background subtraction to separate moving foreground objects (vehicles) from the static background scene.
- **Morphological Operations:** Noise reduction and contour refinement using erosion, dilation, opening, and closing operations.
- **Contour Detection:** Identification of vehicle boundaries using OpenCV's contour detection algorithms.
- **YOLOv8 Object Detection:** Deep learning-based vehicle classification using the YOLOv8 nano model to identify vehicle types (Car, Motorcycle, Truck, Bus, Bicycle).
- **Centroid-Based Tracking:** A lightweight tracking algorithm that associates detections across frames based on Euclidean distance between centroids.
- **Speed Estimation:** Pixel displacement per frame is converted to real-world speed (km/h) using a calibration factor (pixels-per-meter ratio).

### Tools and Technologies

- Python 3.8+
- OpenCV 4.9 (Computer Vision Library)
- NumPy 1.26 (Numerical Computing)
- Ultralytics YOLOv8 (Deep Learning Object Detection)
- PyTorch (Deep Learning Framework)

### Expected Outcome

The system produces an annotated output video with:
- Color-coded bounding boxes around detected vehicles (different colors per vehicle type)
- Vehicle type classification labels (Car, Motorcycle, Truck, Bus, Bicycle)
- Unique tracking IDs for each vehicle
- Real-time speed estimation displayed as overlay text
- On-screen legend showing color-to-type mapping

### Limitations

- Speed accuracy depends on camera calibration and viewing angle.
- Performance may vary under different lighting and weather conditions.
- Requires a static camera for background subtraction to work effectively.
- This is a proof-of-concept and not intended for production traffic enforcement.

### Conclusion

This project demonstrates the feasibility of combining traditional computer vision (background subtraction) with modern deep learning (YOLOv8) for vehicle speed detection and classification. The approach provides a low-cost alternative to traditional hardware-based systems and is suitable for educational purposes and as a foundation for more advanced traffic monitoring solutions.

---

**Keywords:** Computer Vision, Deep Learning, YOLOv8, Vehicle Detection, Vehicle Classification, Speed Estimation, Background Subtraction, OpenCV, Object Tracking
