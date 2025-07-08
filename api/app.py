from fastapi import FastAPI, File, UploadFile
from utils.detector import detect_faces
from utils.encoder import encode_face
from utils.matcher import match_face
from utils.database import load_database
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read())).convert('RGB')
    frame = np.array(image)
    faces = detect_faces(frame)
    db = load_database("embeddings/database.pkl")

    results = []
    for (x, y, w, h), face_img in faces:
        encoding = encode_face(face_img)
        name, confidence = match_face(encoding, db)
        results.append({"name": name, "confidence": round(confidence, 2)})

    return {"results": results}