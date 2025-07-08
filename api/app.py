from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.detector import detect_faces
from utils.encoder import encode_face
from utils.matcher import match_face
from utils.database import load_database
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
import os
import pickle

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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

@app.post("/api/enroll")
async def enroll_face(file: UploadFile = File(...), name: str = Form(...)):
    db_path = "embeddings/database.pkl"
    db = load_database(db_path)

    image = Image.open(BytesIO(await file.read())).convert("RGB")
    frame = np.array(image)
    faces = detect_faces(frame)

    if not faces:
        return {"status": "error", "message": "No face detected."}

    (x, y, w, h), face_img = faces[0]
    embedding = encode_face(face_img)
    db[name] = embedding

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, "wb") as f:
        pickle.dump(db, f)

    return {"status": "success", "message": f"Added {name} to database."}
