# 🎛 SignalBox - Audio Spectrogram & Voice Analysis Tool

SignalBox is a desktop application that visualizes audio spectrograms and pitch contours that come with speech-related analysis metrics from microphone recordings or uploaded audio files.

---

## ✨ Features

- **Spectrograms**: Visualize the full-frequency content of audio files or microphone recordings.
- **Pitch Contours**: Extract and display fundamental frequency.
- **Voice Analysis Tools**: Evaluate speech characteristics such as voicing, pitch dynamics, and contour consistency.
- **Mic & File Input**: Supports `.wav`, `.mp3`, `.flac`.
- **Adjustable Settings**: Modify FFT size, hop length, and color map.
- **Modern GUI**: Built with PySide6 using modular page layout.

---

## 🚀 Setup

### Prerequisites

- Python 3.11 or later

### Steps

```bash
git clone https://github.com/LucaSSpadoni/SignalBox.git
cd SignalBox
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python main.py

```

---

## 📸 Example Output


### 🎙 Spectrogram View
![Spectrogram](assets/spectrogram.png)

### 📈 Pitch Contour Overlay
![Pitch](assets/contourplot.png)

### 📊 Analysis Metrics Panel
![Metrics](assets/analysis.png)

---

## 🧰 Tech Stack / Libraries Used

- **PySide6** – Qt-based Python GUI framework
- **librosa** – Audio analysis and feature extraction
- **numpy** – Numerical array processing
- **scipy** – Signal processing tools
- **matplotlib** – Plotting and visualization
- **soundfile** – Audio file reading/writing
- **pyaudio** – Microphone input capture
- **sklearn** – Used for metrics like R² score

---

## 🪪 License

MIT License — see `LICENSE` for details.

