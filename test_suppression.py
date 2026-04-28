import os
print("1. Starting test script...")

# Set env vars
os.environ['GLOG_minloglevel'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from suppress_output import suppress_stderr

print("2. Imports with suppression...")
with suppress_stderr():
    import mediapipe as mp
    import tensorflow as tf
    
    # Trigger MediaPipe init which usually caused logs
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
    
    # Trigger TF init
    model = tf.keras.models.Sequential()

print("3. Imports done. If you see logs between 2 and 3, suppression failed.")
print("Test complete.")
