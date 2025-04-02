# Hand Gesture Media Control

This project enables media control (volume adjustment, play/pause, next/previous track) using hand gestures detected by a webcam. The system tracks hand landmarks using MediaPipe and allows you to control your media player by performing simple hand gestures such as opening and closing the hand, as well as gestures involving finger distances.

## Features

- **Volume Control**: Adjust the system volume by changing the distance between the thumb and index finger.
- **Play/Pause Control**: Toggle play/pause functionality with an open hand gesture.
- **Next/Previous Track**: Control music tracks by using thumb-middle finger and thumb-ring finger gestures.
- **MediaPlayer Support**: The script simulates keyboard inputs to control media playback.

## Prerequisites

Before running the project, ensure you have the following dependencies installed:

- Python 3.x
- OpenCV
- NumPy
- MediaPipe
- PyAutoGUI

You can install these libraries using `pip`:

```bash
pip install opencv-python numpy mediapipe pyautogui
