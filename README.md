# 👁️ Real-Time Driver Drowsiness Detection System

A real-time computer vision system that detects driver drowsiness through webcam-based eye tracking, using facial landmark detection and the Eye Aspect Ratio (EAR) algorithm to trigger instant alerts before a driver falls asleep at the wheel.

---

## 📌 Problem Statement

Driver fatigue is a major cause of road accidents, especially among truck and bus drivers on long routes in Pakistan. Most existing solutions require expensive hardware. This project explores whether a simple webcam and open-source computer vision tools can provide the same safety benefit.

---

## 🧠 How It Works

1. The webcam continuously captures the driver's face
2. **MediaPipe Face Mesh** (a pretrained deep learning model by Google) detects 468 facial landmarks in real time
3. Six key landmark points around each eye are extracted
4. The **Eye Aspect Ratio (EAR)** is calculated using the distance between these points:

   ```
   EAR = (vertical_distance_1 + vertical_distance_2) / (2 × horizontal_distance)
   ```

   - EAR stays high (~0.20–0.35) when eyes are open
   - EAR drops sharply (~0.0–0.08) when eyes are closed

5. A frame counter tracks how many *consecutive* frames the EAR stays below a threshold (0.20)
6. If eyes stay closed for more than 20 consecutive frames (~0.7–1 second), the system triggers:
   - An on-screen **"DROWSINESS ALERT"** message
   - An audible beep sound

This distinguishes a normal blink (1–2 frames) from genuine drowsiness (sustained eye closure).

---

## 🏗️ Tech Stack

| Component | Technology |
|---|---|
| Face & landmark detection | MediaPipe Face Mesh (Google, pretrained model) |
| Video capture & display | OpenCV |
| Distance calculations | SciPy |
| Alert sound | winsound (Windows built-in) |
| Language / Environment | Python 3.11 |

**Note on Python version:** Python 3.11 was specifically used because MediaPipe's stable API (`mp.solutions.face_mesh`) is not yet fully compatible with newer Python releases (e.g. 3.14), where it throws `AttributeError: module 'mediapipe' has no attribute 'solutions'`. Computer vision libraries like MediaPipe, OpenCV, and SciPy are most stable and well-tested on Python 3.10/3.11.

---

## 📁 Project Structure

```
drowsiness-detector/
│
├── main.py              # Main application - camera capture, landmark detection, EAR logic, alerts
├── requirements.txt      # Python dependencies
└── .gitignore
```

---

## ▶️ Running Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/driver-drowsiness-detection.git
cd driver-drowsiness-detection

# It's recommended to use Python 3.11 for compatibility
pip install -r requirements.txt

# Run the detector
python main.py
```

A window will open showing your webcam feed with the face mesh overlay and live EAR value. Close your eyes for about a second to see the alert trigger. Press `q` to quit.

---

## 🎯 Key Features

- Real-time facial landmark tracking (468 points)
- Custom-built EAR calculation from raw landmark coordinates (not a built-in function — implemented from the geometric formula)
- Frame-based counter logic to filter out normal blinks vs. genuine drowsiness
- Live on-screen EAR value and alert status for transparency during demos
- Audible alert using Windows' built-in sound system

---

## 🔮 Future Improvements

- Add yawning detection (mouth aspect ratio) as a second drowsiness signal
- Log drowsiness events with timestamps for fleet monitoring
- Package as a standalone desktop app (PyInstaller) for real vehicle use
- Add head-pose estimation to detect nodding-off, not just eye closure

---

## 📬 Contact

Built by Abdullah Zahid — feel free to connect on [[LinkedIn](your-linkedin-link)](https://www.linkedin.com/in/abdullah-zahid89/) or reach out with feedback!
