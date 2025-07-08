import cv2
from utils.detector import detect_faces
from utils.encoder import encode_face
from utils.database import load_database, save_database
import sys

name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = detect_faces(frame)
    for (x, y, w, h), face_img in faces:
        encoding = encode_face(face_img)
        db = load_database("embeddings/database.pkl")
        db[name] = encoding
        save_database(db, "embeddings/database.pkl")
        print(f"[INFO] Face for '{name}' added.")
        cap.release()
        exit()