from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.detector import detect_faces
from utils.encoder import encode_face
from utils.matcher import match_face
from utils.database import load_database
from PIL import Image
import numpy as np
from io import BytesIO
import cv2

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recognize")
async def recognize_face(file: UploadFile = File(...)):
    db = load_database("embeddings/database.pkl")
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    frame = np.array(image)
    faces = detect_faces(frame)

    results = []
    for (x, y, w, h), face_img in faces:
        embedding = encode_face(face_img)
        name, confidence = match_face(embedding, db)
        results.append({"name": name, "confidence": confidence, "box": [int(x), int(y), int(w), int(h)]})

    return {"results": results}