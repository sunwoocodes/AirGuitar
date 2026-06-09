# 🎸 Air Guitar System

A computer vision based Air Guitar system that allows users to play virtual guitar chords using hand gestures and strumming motions captured through a webcam.

---

## Demo

<p align="center">
  <img src="docs/Test.gif" width="100%">
</p>

---

## Screenshot

<p align="center">
  <img src="docs/main.png" width="100%">
</p>

---

## Features

The system uses MediaPipe hand tracking to recognize chord gestures with the left hand and perform virtual guitar strumming with the right hand in real time.

### 🎵 Gesture-Based Chord Selection

Different left-hand gestures are mapped to guitar chords:

| Gesture | Chord |
|----------|--------|
| Fist | G Minor 7 |
| Two Fingers | G Major 7 |
| Three Fingers | D Major 7 |
| Open Hand | D Dominant 7 |
| Thumb Up | A Dominant 7 |
| No Gesture | E Minor 7 |

---

### 🎸 Real-Time Strumming Detection

- Right-hand index finger controls strumming
- Detects string crossings in real time
- Supports:
  - Bidirectional Strum
  - Downstrum Only Mode

---

### 🔊 Multi-String Audio Playback

Each chord consists of six individual guitar string samples.

Examples:

```text
Em7_1.wav
Em7_2.wav
...
Em7_6.wav
```

The system plays the corresponding string sound when a virtual string is crossed.

---

### 📷 Hand Tracking

Powered by MediaPipe Hands:

- Two-hand tracking
- Real-time landmark detection
- Finger counting
- Gesture recognition

---

### 📊 Motion Data Logging

During execution:

- Strumming Y-coordinate is recorded
- Data is automatically exported as CSV on exit

Example:

```csv
Time_Seconds,Y_Coordinate
0.01,0.542
0.04,0.547
...
```

---

## Tech Stack

### Computer Vision

- OpenCV
- MediaPipe

### GUI

- CustomTkinter

### Audio

- Pygame Mixer

### Image Processing

- Pillow

### Numerical Computation

- NumPy

---

## Project Structure

```text
AirGuitar/
│
├── src/
│   ├── csv/
│   ├── vision.py
│   ├── logic.py
│   ├── app.py
│   └── audio_handler.py
│
├── gui/
│   ├── rock.png
│   ├── two.png
│   ├── three.png
│   ├── open.png
│   ├── thumb.png
│   └── none.png
│
├── docs/
│   ├── Test.gif
│   └── main2.png
│
├── assets/
│   ├── Em7_1.wav
│   ├── Em7_2.wav
│   ├── ...
│
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/sunwoocodes/AirGuitar.git
cd AirGuitar
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
cd src
python app.py
```

---

## Controls

### Chord Selection

Use your left hand:

- ✊ Fist → G Minor 7
- ✌ Two Fingers → G Major 7
- 🤟 Three Fingers → D Major 7
- ✋ Open Hand → D Dominant 7
- 👍 Thumb Up → A Dominant 7

### Strumming

Use your right-hand index finger to cross the virtual strings.

### Mode Toggle

Click the status indicator:

- Gray → Bidirectional Strum
- Yellow → Downstrum Only

---

## Output

CSV files are automatically saved in:

```text
csv/
```

Example:

```text
hand_data_20260609_153245.csv
```

---

## Future Improvements

- More chord types
- Dynamic fret simulation
- Recording mode
- MIDI output support
- Performance analytics dashboard

---

## License

This project was developed for academic and educational purposes.