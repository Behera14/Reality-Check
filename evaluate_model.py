import os
import tensorflow as tf
import numpy as np
import cv2
from suppress_output import suppress_stderr
import os

# import mediapipe as mp # Removed due to protobuf conflict
import tensorflow as tf

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Suppress Logs
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['MEDIAPIPE_DISABLE_GPU']='1'

# --- Configuration ---
MODEL_PATH = 'models/df_92_v2.h5'
# You need to set these paths to your dataset folders
REAL_VIDEOS_DIR = 'datasets/real' 
FAKE_VIDEOS_DIR = 'datasets/fake'
# ---------------------

print("Initializing OpenCV Haar Cascade...")
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

if face_cascade.empty():
    print("Error: Could not load Haar Cascade!")
else:
    print("Haar Cascade loaded.")

print(f"Loading Model: {MODEL_PATH}...")
with suppress_stderr():
    model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded.")

def extract_and_preprocess(video_path, num_frames=15):
    """Extracts frames, crops faces, and preprocesses for Xception."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    processed_faces = []
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0: return []
    
    indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
    
    current_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        if current_frame in indices:
            # Face Crop Logic (Haar Cascade)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            
            if len(faces) > 0:
                # Get largest face
                x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
                
                # Padding
                pw, ph = int(w*0.2), int(h*0.2)
                frame_h, frame_w, _ = frame.shape
                
                x1, x2 = max(0, x-pw), min(frame_w, x+w+pw)
                y1, y2 = max(0, y-ph), min(frame_h, y+h+ph)
                
                face = frame[y1:y2, x1:x2]
                if face.size > 0:
                    face = cv2.resize(face, (224, 224))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    processed_faces.append(face / 255.0)
        
        current_frame += 1
        if len(processed_faces) >= num_frames: break
        
    cap.release()
    return np.array(processed_faces)

def evaluate_directory(directory, label):
    """Iterates over a directory, predicts, and returns results."""
    results = []
    if not os.path.exists(directory):
        print(f"Warning: Directory {directory} not found.")
        return []
        
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.mp4', '.avi', '.mov'))]
    print(f"Found {len(files)} videos in {directory} (Label: {label})")
    
    for filename in files:
        path = os.path.join(directory, filename)
        try:
            faces = extract_and_preprocess(path)
            if len(faces) == 0:
                print(f"  [Skipped] No faces found in {filename}")
                continue
                
            preds = model.predict(faces, verbose=0)
            avg_pred = np.mean(preds)
            
            # Label 0: Real, 1: Fake (Standard)
            # BUT: server.py logic says >0.5 is FAKE.
            # So: Prediction > 0.5 = FAKE (1). Prediction <= 0.5 = REAL (0).
            
            predicted_label = 1 if avg_pred > 0.5 else 0
            results.append((label, predicted_label))
            
            print(f"  {filename}: {'FAKE' if predicted_label else 'REAL'} (Conf: {avg_pred:.2f})")
            
        except Exception as e:
            print(f"  [Error] {filename}: {e}")
            
    return results

# Assume Label schema: 0 = REAL, 1 = FAKE
print("\n--- Evaluating Real Videos ---")
real_results = evaluate_directory(REAL_VIDEOS_DIR, 0)

print("\n--- Evaluating Fake Videos ---")
fake_results = evaluate_directory(FAKE_VIDEOS_DIR, 1)

all_results = real_results + fake_results

if not all_results:
    print("\nNo videos processed. Please check your dataset paths.")
else:
    y_true = [r[0] for r in all_results]
    y_pred = [r[1] for r in all_results]
    
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    
    print("\n=== Evaluation Report ===")
    print(f"Exact Accuracy: {acc * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(f"True Negatives (Correct Real): {cm[0][0]}")
    print(f"False Positives (Real as Fake): {cm[0][1]}")
    print(f"False Negatives (Fake as Real): {cm[1][0]}")
    print(f"True Positives (Correct Fake):  {cm[1][1]}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=['REAL', 'FAKE']))
