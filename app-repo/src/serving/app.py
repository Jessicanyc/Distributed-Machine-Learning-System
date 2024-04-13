from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    processed_data = preprocess(input_data)  # Assume preprocess is a function you define
    
    # Forward the processed data to TensorFlow Serving
    tf_serving_url = "http://tensorflow-serving:8501/v1/models/my_model:predict"
    response = requests.post(tf_serving_url, data=json.dumps({"instances": processed_data}))
    
    predictions = response.json()
    final_response = postprocess(predictions)  # Assume postprocess is another function you define
    
    return jsonify(final_response)

def preprocess(data):
    # Process raw data to the format TensorFlow Serving expects
    return data  # Simplified for illustration

def postprocess(data):
    # Handle processing of TensorFlow Serving responses
    return data  # Simplified for illustration

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
