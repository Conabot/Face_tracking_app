from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
import face_recognition
from database import connect_db

app = Flask(__name__)

UPLOAD_FOLDER = "static/images/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-face', methods=['POST'])
def save_face():
    """Saves face image and encodes it in the database."""
    file = request.files['image']
    name = request.form.get('name')

    # Save image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Encode face
    encoding = face_recognition.face_encodings(face_recognition.load_image_file(filepath))[0]
    
    # Save to DB
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faces (name, encoding) VALUES (%s, %s)", (name, encoding.tobytes()))
    conn.commit()
    conn.close()

    return jsonify({"status": "Face saved!"})

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    """Compares uploaded face with stored faces."""
    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Encode new face
    new_encoding = face_recognition.face_encodings(face_recognition.load_image_file(filepath))[0]

    # Fetch known faces
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM faces")
    rows = cursor.fetchall()
    conn.close()

    # Compare with known faces
    known_encodings = [np.frombuffer(row[1], dtype=np.float64) for row in rows]
    known_names = [row[0] for row in rows]

    results = face_recognition.compare_faces(known_encodings, new_encoding)

    if True in results:
        match_index = results.index(True)
        return jsonify({"status": "Match found!", "name": known_names[match_index]})
    else:
        return jsonify({"status": "No match found."})

if __name__ == '__main__':
    app.run(debug=True)

