# Frequently Asked Questions (FAQ)

---

## Non-Technical Questions

### Q1: What does this project do?

**A:** This system watches a video of a road and automatically detects vehicles (cars, bikes, trucks, buses), identifies what type of vehicle it is, and estimates how fast each vehicle is moving. It draws colored boxes around each vehicle and shows the speed on screen.

---

### Q2: Do I need any special camera or hardware?

**A:** No. This works with any standard video file (MP4 format). For the POC, you just need a regular computer with Python installed. No special camera, GPU, or internet connection is required.

---

### Q3: How do I run this project?

**A:** 
1. Place your video file as `input/footage.mp4`
2. Double-click `start.bat`
3. Wait for setup to complete (first time takes a few minutes)
4. The processed video will be saved in the `output/` folder

That's it. No coding knowledge needed.

---

### Q4: What types of vehicles can it detect?

**A:** The system can identify five types:
- Cars
- Motorcycles/Bikes
- Bicycles
- Buses
- Trucks

Each type gets a different colored box in the output video.

---

### Q5: How accurate is the speed measurement?

**A:** This is a proof-of-concept, so the speed values are estimates. Accuracy depends on:
- How the camera is positioned (angle, height)
- The calibration value set in the configuration
- Video quality and frame rate

For a production system, proper camera calibration would give ±5 km/h accuracy.

---

### Q6: Can this be used for issuing traffic fines?

**A:** Not in its current state. This is a college project / proof-of-concept. For legal enforcement, you would need:
- Certified accuracy (validated against radar)
- License plate recognition
- Tamper-proof evidence chain
- Government approval and certification

However, the technology foundation is the same as what commercial systems use.

---

### Q7: Does it work at night or in rain?

**A:** The current POC works best in daylight with clear visibility. Night and rain performance is limited. A production version would use:
- Infrared (IR) cameras for night
- Model fine-tuning for adverse weather
- Multiple detection strategies

---

### Q8: Can it work with live CCTV cameras?

**A:** The current version processes pre-recorded video files only. However, the underlying technology (OpenCV, YOLO) fully supports live camera streams (RTSP, HTTP). This would be a straightforward enhancement for a production version.

---

### Q9: Is this legal to use?

**A:** For educational and research purposes, yes. For actual traffic monitoring:
- Private property (parking lots, campuses) — generally fine
- Public roads — requires government authorization
- Privacy laws may apply depending on your jurisdiction

Always check local regulations before deploying surveillance systems.

---

### Q10: How much would it cost to make this a real product?

**A:** See the Future Roadmap document for detailed cost analysis. In summary:
- Development: ₹50-65 lakhs (~$60,000-80,000) over 12 months
- Hardware per camera point: ₹38,000-80,000 (~$465-980)
- Monthly cloud costs: ₹23,000-48,000 (~$277-575)

The key advantage is that it works with existing cameras — no new camera hardware needed.

---

### Q11: Who are the competitors in this space?

**A:** Major players include:
- **Hikvision** — Chinese company, hardware + software
- **Dahua** — Chinese company, integrated cameras
- **Genetec** — Canadian, enterprise video analytics
- **BriefCam** — Video synopsis and analytics
- **Vehant Technologies** — Indian, traffic enforcement

Our advantage: pure software solution that works with any existing camera.

---

### Q12: What's the market opportunity?

**A:** The global intelligent traffic management market is ~$15 billion (2025) growing at 12-15% annually. In India alone, smart city projects have allocated thousands of crores for traffic management. The key opportunity is the millions of existing CCTV cameras that currently have no AI analytics.

---

---

## Technical Questions

### Q13: What algorithm is used for vehicle detection?

**A:** Two approaches work together:
1. **MOG2 Background Subtraction** — Separates moving objects from the static background. Fast and lightweight but requires a static camera.
2. **YOLOv8 Nano** — Deep learning object detection for vehicle classification. Runs every 5 frames to balance performance with accuracy.

The background subtraction handles motion detection (fast), while YOLO handles classification (accurate).

---

### Q14: Why use background subtraction instead of YOLO for everything?

**A:** Performance. Background subtraction is computationally cheap and runs on every frame. YOLO is more expensive (especially on CPU). The hybrid approach gives us:
- Fast motion detection on every frame (MOG2)
- Accurate classification periodically (YOLO every 5 frames)
- Graceful fallback if YOLO model is unavailable

For a GPU-equipped production system, you could use YOLO for everything.

---

### Q15: How does the tracking work?

**A:** Centroid-based tracking:
1. Calculate the center point (centroid) of each detected bounding box
2. Compare with centroids from the previous frame
3. Match based on minimum Euclidean distance (threshold: 80 pixels)
4. If a vehicle isn't seen for 10 frames, remove its track
5. New unmatched detections get new IDs

**Limitation:** Can fail with occlusion or very fast-moving vehicles. Production systems use DeepSORT or ByteTrack which incorporate appearance features.

---

### Q16: How is speed calculated?

**A:** 
```
speed (km/h) = (pixel_displacement / pixels_per_meter) × fps × 3.6
```

Steps:
1. Track the centroid position over the last 10 frames
2. Calculate average pixel displacement per frame
3. Convert pixels to meters using the calibration factor
4. Convert meters/frame to meters/second using FPS
5. Convert to km/h (multiply by 3.6)

**Critical:** The `PIXELS_PER_METER` value in `config.py` must be calibrated for your specific camera setup.

---

### Q17: How do I calibrate the speed measurement?

**A:** 
1. Identify a known distance in your video (e.g., lane markings are typically 3m apart, or measure a known object)
2. Count how many pixels that distance spans in the video frame
3. Calculate: `PIXELS_PER_METER = pixel_distance / real_distance_in_meters`
4. Update the value in `src/config.py`

Example: If lane markings (3m apart) span 24 pixels → `PIXELS_PER_METER = 24 / 3 = 8.0`

---

### Q18: Why does it take a few seconds before vehicles are detected?

**A:** The MOG2 background subtractor needs time to "learn" what the background looks like. It builds a statistical model over the first 50-100 frames. During this learning period, everything appears as foreground, so detections are unreliable.

**Fix:** You can reduce `BG_SUBTRACTOR_HISTORY` in config.py for faster learning, but this may increase false positives.

---

### Q19: The bounding boxes are flickering or unstable. Why?

**A:** Common causes:
- **Shadows:** MOG2 detects shadows as foreground. The system removes them via thresholding, but some may persist.
- **Noise:** Small contours from leaves, birds, etc. Increase `MIN_CONTOUR_WIDTH/HEIGHT` in config.
- **Fragmentation:** A single vehicle detected as multiple parts. Increase dilation iterations or morphological kernel size.
- **Tracking jumps:** Centroid tracker may lose and re-acquire vehicles. Reduce `MAX_DISTANCE_THRESHOLD` for tighter matching.

---

### Q20: Can I use a different YOLO model?

**A:** Yes. You can use any Ultralytics model:
- `yolov8n.pt` — Nano (current, fastest, least accurate)
- `yolov8s.pt` — Small (good balance)
- `yolov8m.pt` — Medium (more accurate, slower)
- `yolov8l.pt` — Large (high accuracy, needs GPU)
- `yolov8x.pt` — Extra large (best accuracy, needs good GPU)

Change `YOLO_MODEL_PATH` in `config.py` and download the model accordingly.

---

### Q21: It's running very slowly on my computer. How to speed it up?

**A:** Options:
1. **Reduce resolution:** Resize frames before processing (add `cv2.resize()` in main.py)
2. **Skip frames:** Process every 2nd or 3rd frame instead of every frame
3. **Increase YOLO interval:** Change from every 5 frames to every 10-15 frames
4. **Use smaller ROI:** Reduce the detection region in config.py
5. **Disable display:** Comment out `cv2.imshow()` — rendering takes time
6. **Use GPU:** Install CUDA-enabled PyTorch for faster YOLO inference

---

### Q22: How do I change the detection region (ROI)?

**A:** Edit `src/config.py`:
```python
ROI_Y_START = 200  # Top boundary (pixels from top)
ROI_Y_END = 600    # Bottom boundary (pixels from top)
```

Only vehicles within this vertical band are detected. Adjust based on where vehicles appear in your specific video.

---

### Q23: The YOLO model download failed. Can the project still run?

**A:** Yes. If the YOLO model is not available, the system falls back to **size-based classification**:
- Small objects → Motorcycle
- Medium objects → Car
- Large objects → Truck/Bus

Detection and tracking still work via background subtraction. Only the vehicle type label will be less accurate.

---

### Q24: What Python version is required?

**A:** Python 3.8 or higher. Tested with Python 3.11. The `start.bat` file checks for Python automatically and shows an error message if it's not installed.

---

### Q25: Can I process multiple videos?

**A:** Currently, the system is hardcoded to process `input/footage.mp4`. To process a different video:
1. Rename your video to `footage.mp4` and place in `input/`, OR
2. Edit `run.py` and change the `INPUT_VIDEO` path

For batch processing multiple videos, you would need to modify `run.py` to loop through files in the input directory.

---

### Q26: What video formats are supported?

**A:** Any format supported by OpenCV's VideoCapture, which includes:
- MP4 (H.264, H.265)
- AVI
- MOV
- MKV
- WMV

MP4 with H.264 codec is recommended for best compatibility.

---

### Q27: How do I add a new vehicle type?

**A:** 
1. The YOLO model detects COCO classes. Check if your vehicle type exists in COCO (80 classes).
2. If it does, add the class ID to `VEHICLE_CLASS_MAP` in `vehicle_classifier.py`
3. Add a color entry in `VEHICLE_COLORS` in `config.py`

For custom vehicle types not in COCO (e.g., auto-rickshaw), you would need to fine-tune the YOLO model on custom training data.

---

### Q28: What's the IoU matching and why is it needed?

**A:** IoU (Intersection over Union) measures how much two bounding boxes overlap:
```
IoU = Area of Overlap / Area of Union
```

It's used to match YOLO classifications (which run every 5 frames) to the continuously tracked vehicles (from background subtraction). If a YOLO detection overlaps >30% with a tracked vehicle's bounding box, the classification is assigned to that vehicle.

---

### Q29: Can this work with a moving camera (dashcam)?

**A:** Not with the current approach. Background subtraction requires a **static camera** because it models the background over time. With a moving camera, the entire scene changes every frame.

For dashcam/moving camera scenarios, you would need:
- YOLO-only detection (no background subtraction)
- Optical flow for motion estimation
- GPS data for speed reference

---

### Q30: How do I contribute or extend this project?

**A:** The modular architecture makes it easy to extend:
- **Better detection:** Replace `vehicle_detector.py` with a YOLO-only detector
- **Better tracking:** Replace `vehicle_tracker.py` with DeepSORT implementation
- **Better speed:** Add perspective transform in `speed_estimator.py`
- **New features:** Add license plate recognition, lane detection, or violation alerts

Each module has a clear interface (input/output), so you can swap implementations without affecting other components.

---

## Troubleshooting

### "Python is not installed or not in PATH"

**Solution:** Download Python from https://www.python.org/downloads/ and during installation, check the box "Add Python to PATH". Restart your computer after installation.

---

### "Input file not found"

**Solution:** Make sure your video file is named exactly `footage.mp4` and placed inside the `input/` folder within the project directory.

---

### "Failed to install dependencies"

**Solution:** 
- Check your internet connection
- Try running: `pip install --upgrade pip` then `pip install -r requirements.txt`
- If behind a corporate proxy, configure pip proxy settings

---

### "Cannot open video file"

**Solution:** 
- Verify the video file is not corrupted (try playing it in VLC)
- Ensure it's a supported format (MP4 recommended)
- Check file permissions

---

### "YOLO model not found"

**Solution:** Run `python download_model.py` manually. If it fails:
- Check internet connection
- Try: `pip install ultralytics` then run the script again
- As a last resort, the system will still work with size-based fallback classification

---

### Video window is black or frozen

**Solution:**
- Wait 2-3 seconds — the background model needs time to learn
- Check if the video has actual content (not a blank recording)
- Try pressing any key on the video window to advance
- If the window says "Not Responding", your CPU may be too slow — try reducing video resolution
