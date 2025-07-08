import cv2
import numpy as np
from mtcnn import MTCNN

detector = MTCNN()

def detect_faces(image):
    faces = []
    results = detector.detect_faces(image)
    for res in results:
        x, y, w, h = res['box']
        face_img = image[y:y+h, x:x+w]
        faces.append(((x, y, w, h), face_img))
    return faces