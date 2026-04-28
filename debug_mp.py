import mediapipe as mp
print("Init MP")
mp_face_mesh = mp.solutions.face_mesh
print("Create FaceMesh")
try:
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=False,
        min_detection_confidence=0.5
    )
    print("Success")
except Exception as e:
    print(f"Failed: {e}")
