# smart-recycling-bin
An AI-powered smart waste sorting system using Edge Impulse, Python, and Arduino. It classifies objects in real-time via webcam, automatically routes them using a servo motor, and provides dynamic audio feedback with a DFPlayer Mini.
# Smart AI Waste Sorter

An intelligent waste classification system that leverages Computer Vision and Machine Learning at the edge to automatically sort items into distinct categories.

This project integrates a Python backend running an Edge Impulse model with an advanced Arduino board via RPC (Remote Procedure Call). It processes real-time video, mechanically routes waste using a servo motor, and provides dynamic audio feedback.

## Features
* **Real-Time Vision Processing:** Uses a USB webcam and Python to run ML inference.
* **Local Web Dashboard:** A WebSockets-based interface (`Socket.IO`) to monitor the camera feed, adjust confidence thresholds, and view detection logs.
* **Hardware-in-the-Loop Control:** Seamless communication between Python and the Arduino MCU using the `Arduino_RouterBridge` library.
* **Automated Sorting:** Drives a servo motor to route waste into three positions (15°, 90°, 155°).
* **Interactive Audio Feedback:** Uses a DFPlayer Mini over hardware serial (`Serial1`) to play specific voice tracks for each detected material, alongside a buzzer for metal alerts.
* **Manual Override:** Includes a hardware interrupt (push button with debounce) allowing operators to manually cycle through servo positions.

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

    
