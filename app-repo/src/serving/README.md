## Custom Application Logic for model inference 

additional processing needed before sending data to TensorFlow Serving (such as preprocessing input data, formatting the request, or handling postprocessing after getting predictions), this logic is typically implemented in a separate application. This application might be a Python Flask app, which you might containerize and deploy separately.

### Preprocessing: 

the Flask app might accept raw data from clients, preprocess it into the format TensorFlow Serving expects, and then forward it to TensorFlow Serving.
Request Forwarding: The Flask app sends a POST request to TensorFlow Serving using the processed data.
Postprocessing: After receiving the predictions from TensorFlow Serving, your Flask app can further process these results (like formatting or integrating them into a larger response) before sending them back to the client.

### Data Flow:

- A client sends a request to your Flask app.
- The Flask app processes (preprocesses) this data.
- It sends a new request to TensorFlow Serving (http://tensorflow-serving:8501/v1/models/my_model:predict).
- TensorFlow Serving makes predictions and returns them to the Flask app.
- The Flask app may postprocess the predictions and sends the final response back to the client.

the Flask app acts as a middleware that handles preprocessing and postprocessing, while TensorFlow Serving is focused solely on loading TensorFlow models and performing predictions