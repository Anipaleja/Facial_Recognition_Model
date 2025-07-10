import sqlite3
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from email.message import EmailMessage
import smtplib
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(email: str, password: str):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    if c.fetchone():
        conn.close()
        return "exists"
    hashed = get_password_hash(password)
    c.execute("INSERT INTO users (email, password, verified) VALUES (?, ?, ?)", (email, hashed, 0))
    conn.commit()
    conn.close()
    return "created"

def authenticate_user(username: str, password: str):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT email, password, verified FROM users WHERE email = ?", (username,))
    result = c.fetchone()
    conn.close()
    if not result:
        return False
    email, hashed_password, verified = result
    if not verify_password(password, hashed_password):
        return False
    if verified == 0:
        raise HTTPException(status_code=403, detail="Email not verified.")
    return (email,)

def get_current_user(token: str = Depends(oauth2_scheme)):
    return token

def send_verification_email(email: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = "noreply@yourapp.com"
    msg["To"] = email
    msg.set_content("Thanks for signing up. Click the link to verify your email: http://localhost:8000/verify?email=" + email)

    # WARNING: Only for local dev — replace with SendGrid or secure SMTP for production
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)
