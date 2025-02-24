import tensorflow as tf
import cv2
import numpy as np


class DeepFakeDetector:
    def __init__(self, model_path):
        """Initialize the DeepFake detector with a trained model."""
        self.model = tf.keras.models.load_model(model_path)

    def preprocess_frame(self, frame):
        """Preprocess an image for model input."""
        frame = cv2.resize(frame, (224, 224))
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        elif frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = frame.astype(np.float32) / 255.0
        frame = np.expand_dims(frame, axis=0)

        return frame

    def predict_frame(self, frame):
        """Predict whether an image is real or fake."""
        processed_frame = self.preprocess_frame(frame)
        prediction = self.model.predict(processed_frame)[0][0]

        # Log raw prediction value
        print(f"Raw prediction value: {prediction}")

        result = "Real" if prediction > 0.7 else "Fake"  # Lower threshold to 0.4 for testing
        print(f"Prediction result: {result} (Threshold: 0.4)")

        return result, prediction
