from fastapi import FastAPI, UploadFile, File, Request, Form, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from utils.detector import detect_faces
from utils.encoder import encode_face
from utils.matcher import match_face
from utils.database import load_database
from utils.auth import create_user, authenticate_user, get_current_user, send_verification_email
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
import os
import pickle
import sqlite3
from typing import Optional
from jose import JWTError, jwt
print("python-jose is installed and working")

from fastapi.security.utils import get_authorization_scheme_param

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
def startup():
    if not os.path.exists("users.db"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, verified INTEGER)''')
        conn.commit()
        conn.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    token = None
    auth = request.headers.get("Authorization")
    user = None
    if auth:
        scheme, param = get_authorization_scheme_param(auth)
        if scheme.lower() == "bearer":
            token = param
            try:
                user = get_current_user(token)
            except JWTError:
                user = None
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
@app.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/token")
async def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user[0], "token_type": "bearer"}

@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...)):
    result = create_user(email, password)
    if result == "exists":
        return {"status": "error", "message": "User already exists"}
    send_verification_email(email)
    return {"status": "success", "message": "Registration successful. Please verify your email."}

@app.post("/api/recognize")
async def recognize_face(file: UploadFile = File(...), user: str = Depends(get_current_user)):
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
async def enroll_face(file: UploadFile = File(...), name: str = Form(...), user: str = Depends(get_current_user)):
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