import numpy as np
from keras_facenet import FaceNet

embedder = FaceNet()

def encode_face(face_img):
    return embedder.embeddings([face_img])[0]
