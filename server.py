from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the model from the pickle file
try:
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    print("Model file not found. Please check the file path.")
    exit(1)
except pickle.UnpicklingError:
    print("Error loading the model. The file may be corrupt.")
    exit(1)

# Variable to store the latest prediction
latest_prediction = {"prediction": "NotDefined"}

@app.route('/predict', methods=['POST'])
def predict():
    global latest_prediction  # Access the global variable
    
    data = request.get_json()
    
    # Check if 'features' key is in JSON data
    if not data or 'features' not in data:
        return jsonify({'error': 'No features provided in request'}), 400
    
    try:
        features = data['features']
        features_array = np.array([features])
        
        confidence_threshold = 0.70
        prediction = model.predict(features_array)
        y_proba = model.predict_proba(features_array)
        
        if max(y_proba[0]) >= confidence_threshold:
            latest_prediction = {'prediction': prediction[0]}
        else:
            latest_prediction = {'prediction': "NotDefined"}
        
        # Respond to the receiver ESP32
        return jsonify(latest_prediction)
    
    except Exception as e:
        # General exception for any runtime issues
        return jsonify({'error': str(e)}), 500

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    # Allow another ESP32 to fetch the latest prediction
    return jsonify(latest_prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)