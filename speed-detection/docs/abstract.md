# Abstract

## Vehicle Speed Detection System Using Computer Vision

### Problem Statement

Traffic monitoring and speed enforcement are critical for road safety. Traditional speed detection methods rely on expensive hardware such as radar guns and inductive loop detectors. This project proposes a cost-effective, software-based approach to vehicle speed estimation using computer vision techniques applied to standard video footage.

### Objective

To design and implement a vehicle speed detection system that can:

1. Detect moving vehicles (cars, bikes, and other motorized vehicles) in video footage.
2. Track detected vehicles across consecutive video frames.
3. Estimate the speed of each tracked vehicle in real-time.

### Methodology

The system employs the following techniques:

- **Background Subtraction (MOG2):** Gaussian Mixture Model-based background subtraction is used to separate moving foreground objects (vehicles) from the static background scene.
- **Morphological Operations:** Noise reduction and contour refinement using erosion, dilation, opening, and closing operations.
- **Contour Detection:** Identification of vehicle boundaries using OpenCV's contour detection algorithms.
- **Centroid-Based Tracking:** A lightweight tracking algorithm that associates detections across frames based on Euclidean distance between centroids.
- **Speed Estimation:** Pixel displacement per frame is converted to real-world speed (km/h) using a calibration factor (pixels-per-meter ratio).

### Tools and Technologies

- Python 3.8+
- OpenCV 4.x (Computer Vision Library)
- NumPy (Numerical Computing)

### Expected Outcome

The system produces an annotated output video with:
- Bounding boxes around detected vehicles
- Unique tracking IDs for each vehicle
- Real-time speed estimation displayed as overlay text

### Limitations

- Speed accuracy depends on camera calibration and viewing angle.
- Performance may vary under different lighting and weather conditions.
- This is a proof-of-concept and not intended for production traffic enforcement.

### Conclusion

This project demonstrates the feasibility of using computer vision for vehicle speed detection as a low-cost alternative to traditional hardware-based systems. The approach is suitable for educational purposes and serves as a foundation for more advanced traffic monitoring solutions.

---

**Keywords:** Computer Vision, Vehicle Detection, Speed Estimation, Background Subtraction, OpenCV, Object Tracking
