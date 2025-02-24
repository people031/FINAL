from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import cv2
from werkzeug.utils import secure_filename
from deepfake_detector import DeepFakeDetector

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key in production

# Load the trained deepfake detection model
detector = DeepFakeDetector("D:\clg\VSK\deepfake_detector_model.h5")

# Allowed file extensions (Only images)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy users database (Replace this with a proper database)
users = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Renders the index page (always first page)."""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Renders the dashboard only if user is logged in."""
    if 'user' not in session:
        return redirect(url_for('index'))  # Redirect to index if not logged in
    return render_template('dashboard.html')


@app.route('/signup', methods=['POST'])
def signup():
    """Handles user signup."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = password
    return jsonify({"message": "Signup successful"}), 200


@app.route('/login', methods=['POST'])
def login():
    """Handles user login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users.get(username) == password:
        session['user'] = username
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/predict', methods=['POST'])
def predict():
    """Handles image upload and deepfake prediction."""
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load image
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({"error": "Invalid image format"}), 400

        # Get prediction and confidence
        result, prediction = detector.predict_frame(image)
        confidence = float(prediction) if result == "Real" else float(1 - prediction)

        return jsonify({
            "prediction": result,
            "confidence": f"{confidence * 100:.2f}%",
            "color": "green" if result == "Real" else "red",
            "image_url": f"/static/uploads/{filename}"
        })

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/logout')
def logout():
    """Logs out the user."""
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
