import os
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS

# ========== CONFIG ==========
class_names = ['Zinc', 'iron', 'normal', 'vitamin_A', 'vitamin_B', 'vitamin_C', 'vitamin_D', 'vitamin_E']
MODEL_PATH = "best_alexnet_varsize.h5"

# Flask setup with CORS (taaki frontend bina roke baat kar sake)
app = Flask(__name__)
CORS(app)

# AI Model Load karenge
print("Loading trained AlexNet model...")
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
else:
    print(f"ERROR: {MODEL_PATH} file nahi mili! Check kijiye.")

# Readable Labels Map
label_map = {
    "vitamin_A": "Vitamin A",
    "vitamin_B": "Vitamin B",
    "vitamin_C": "Vitamin C",
    "vitamin_D": "Vitamin D",
    "vitamin_E": "Vitamin E",
    "iron": "Iron",
    "Zinc": "Zinc",
    "normal": "Normal"
}

# 🚀 FRONTEND SE PHOTO LENE WALA ASLI RAASTA (ROUTE)
@app.route('/predict', methods=['POST'])
@app.route('/api/analyze', methods=['POST'])  # Dono raaste open rakhe hain
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Photo ko read aur process karenge
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # AI Model ke liye resize aur normalize
        img_resized = cv2.resize(img, (400, 400))
        img_scaled = img_resized.astype('float32') / 255.0
        img_expanded = np.expand_dims(img_scaled, axis=0)
        
        # Prediction nikalenge
        preds = model.predict(img_expanded, verbose=0)[0]
        idx = np.argmax(preds)
        confidence = float(preds[idx])
        predicted_class = class_names[idx]
        readable = label_map.get(predicted_class, predicted_class)
        
        if readable == "Normal":
            diagnosis = "Your eyes appear normal — no deficiency detected."
        else:
            diagnosis = f"You have {readable} deficiency."
            
        # Frontend ko ye data return karenge
        response_data = {
            "success": True,
            "predicted_class": predicted_class,
            "readable_label": readable,
            "confidence": f"{confidence * 100:.2f}%",
            "diagnosis": diagnosis,
            "message": "Analysis successful"
        }
        print(f"Prediction Done: {readable} ({confidence * 100:.2f}%)")
        return jsonify(response_data)

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Vitamin Deficiency Prediction Server on Port 5000...")
    app.run(host="127.0.0.1", port=5000, debug=True)