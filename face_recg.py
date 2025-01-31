import cv2
import numpy as np
import face_recognition
import os

def encode_face(image_path):
    """Encodes the face from an image and returns the embedding vector."""
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    return face_encodings[0] if face_encodings else None

def compare_faces(known_encodings, new_encoding):
    """Compares a new face with known faces."""
    results = face_recognition.compare_faces(known_encodings, new_encoding)
    return results
