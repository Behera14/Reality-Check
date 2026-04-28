# REALITY CHECK: Multimodal Deepfake Detection

A robust Flask web application for detecting deepfake content across various media types using state-of-the-art AI models, including ResNet-50, LSTM, EfficientNet-B0, and Audio Neural Networks.

## Features

- **Video Detection**: Upload videos (MP4, AVI, MOV) to detect deepfakes using temporal frame analysis.
- **Image Detection**: Analyze static images for AI manipulation and synthetic generation.
- **Audio Detection**: Detect AI-generated voice clones, text-to-speech, and manipulated audio (WAV, MP3).
- **Visual Analysis**: Temporal heatmaps showing frame-by-frame detection confidence.
- **User Authentication**: Secure Login and Sign Up functionality.
- **Modern Interface**: Premium light-themed glassmorphism design.

---

## 🚀 How to Run the Project

Follow these exact steps to run the project smoothly on your Windows machine.

### 1. Requirements
Ensure you have **Python 3.10** installed on your system. This specific version is required for compatibility with the PyTorch and TensorFlow dependencies.

### 2. Activate the Virtual Environment
Open your terminal (PowerShell or Command Prompt), navigate to the project directory, and activate the virtual environment:

```powershell
# Navigate to the project directory
cd "c:\Users\hp\Desktop\Final year Project\dfd"

# Activate the virtual environment
.\venv\Scripts\activate
```
*(You should see `(venv)` appear at the start of your terminal prompt indicating it is active).*

### 3. Install Dependencies (If not already installed)
With the environment active, install all required packages:
```powershell
pip install -r requirements.txt
```

### 4. Run the Server
Start the Flask application:
```powershell
python server.py
```

### 5. Access the Application
Once the server is running, open your web browser and navigate to:
**http://127.0.0.1:10000**

*(Note: The application runs on port 10000, not the default 5000).*

---

## Project Structure

```text
├── server.py           # Main Flask application and routing
├── models.py           # Database models
├── models/             # Pre-trained AI model weights (audio_classifier.h5, best_model-v3.pt, etc.)
├── templates/          # HTML templates
├── static/             # CSS and static files (index.css)
└── requirements.txt    # Python dependencies
```

## Troubleshooting
- **ModuleNotFoundError**: Ensure your virtual environment `(venv)` is activated before running the server.
- **Model Loading Errors**: Ensure that all `.h5` and `.pt` weight files are present in the `models/` directory.
- **Port already in use**: If port 10000 is blocked, you can modify the `port` parameter at the bottom of `server.py`.
