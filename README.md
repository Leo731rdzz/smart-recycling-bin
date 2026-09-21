# Smart AI Waste Sorter

An intelligent waste classification system that leverages Computer Vision and Machine Learning at the edge to automatically sort items into distinct categories.

This project integrates a Python backend running an Edge Impulse model with an advanced Arduino board via RPC (Remote Procedure Call). It processes real-time video, mechanically routes waste using a servo motor, and provides dynamic audio feedback.

## Features
* **Real-Time Vision Processing:** Uses a USB webcam and Python to run ML inference.
* **Arduino AppLab & Bricks:** Built using the Arduino AppLab ecosystem, utilizing modular App Bricks for rapid integration of Web UIs and video object detection.
* **Local Web Dashboard:** A WebSockets-based interface (`Socket.IO`) to monitor the camera feed, adjust confidence thresholds, and view detection logs.
* **Hardware-in-the-Loop Control:** Seamless communication between Python and the Arduino MCU using the `Arduino_RouterBridge` library.
* **Automated Sorting:** Drives a servo motor to route waste into three positions (15°, 90°, 155°).
* **Interactive Audio Feedback:** Uses a DFPlayer Mini over hardware serial (`Serial1`) to play specific voice tracks for each detected material.
* **Manual Override:** Includes a hardware interrupt (push button with debounce) allowing operators to manually cycle through servo positions.

## Software Ecosystem & Machine Learning
### Arduino AppLab & Edge Impulse Integration
This project is built on top of the **Arduino AppLab** framework. The Python backend utilizes **Arduino App Bricks** (`arduino.app_bricks`) to simplify complex tasks:
* **Video Object Detection Brick:** Connects seamlessly to a local **Edge Impulse** runner (`ei-video-obj-detection-runner`). The model is trained on the Edge Impulse Studio to recognize 6 classes (Apple, Plastic, Paper, PET, Can, Egg) and deployed to run locally. The Python script establishes a WebSocket/TCP connection to fetch real-time bounding boxes and confidence metrics.
* **Web UI Brick:** Instantiates a local server to serve the HTML/JS/CSS assets and handle asynchronous events (like threshold slider adjustments) via WebSockets.

### Dependencies & Libraries
**Python:**
* `arduino-app-utils` (Handles the RPC Bridge and App lifecycle)
* `arduino-app-bricks` (Web UI and Video Object Detection)
* `threading` & `time` (For non-blocking hardware operations)

**Arduino (C++):**
* `Arduino_RouterBridge` (RPC communication with Python)
* `Servo` (Motor control)
* `DFRobotDFPlayerMini` (Audio control)

## Hardware Requirements
* Advanced Arduino Board (e.g., Portenta/GIGA with MPU/MCU architecture)
* USB Webcam
* Servo Motor
* DFPlayer Mini MP3 Module + Micro SD Card (FAT32)
* Speaker & Buzzer
* Push Button

## Pinout & Wiring
| Component | Arduino Pin | Notes |
| :--- | :--- | :--- |
| **Servo Motor** | `D9` | Requires common GND with external power supply |
| **Buzzer** | `D8` | Active buzzer |
| **Push Button** | `D2` | Connected to GND (Uses `INPUT_PULLUP`) |
| **DFPlayer TX** | `D0 (RX)` | Hardware Serial1 (Crossed connection) |
| **DFPlayer RX** | `D1 (TX)` | Hardware Serial1 (Crossed connection) |

*Note: SD Card must contain a folder named `mp3` with tracks formatted as `0001.mp3`, `0002.mp3`, etc.*

## Project Structure
```text
├── main.py           # Python backend (Vision processing & Bridge logic)
├── sketch.ino        # Arduino firmware (Hardware control)
├── README.md         # Project documentation
└── assets/           # Web interface files
    ├── index.html
    ├── style.css
    └── app.js
    
