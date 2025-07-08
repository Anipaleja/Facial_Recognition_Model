#!/bin/bash

# Facial Recognition Project Setup Script

echo "[INFO] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

echo "[INFO] Creating directory structure..."
mkdir -p data embeddings models demo utils api

echo "[INFO] Setup complete. Activate your environment with:"
echo "source venv/bin/activate"
