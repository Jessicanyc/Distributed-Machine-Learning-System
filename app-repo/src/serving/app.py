from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import requests
import json

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic models for structured data validation and documentation
class InputData(BaseModel):
    # Example fields; you should adjust these to match the structure expected by TensorFlow Serving
    example_field: float
    another_field: int

class OutputData(BaseModel):
    # Define output structure based on TensorFlow Serving response
    prediction: float

@app.post("/predict/", response_model=OutputData)
async def predict(input_data: InputData):
    processed_data = preprocess(input_data.dict())  # Convert Pydantic model to dict and preprocess
    
    # Forward the processed data to KServe
    kserve_url = "http://<kservice-name>.<namespace>.example.com/v1/models/<model-name>:predict"
    response = requests.post(kserve_url, json={"instances": [processed_data]})
   
    # Check for errors in KServe response
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error processing the request")

    predictions = response.json()
    final_response = postprocess(predictions)  # Assume postprocess is another function you define
    
    return OutputData(prediction=final_response)

def preprocess(data):
    # Process raw data to the format TensorFlow Serving expects
    # Example processing; adjust this as needed based on your model's requirements
    return data  # Simplified for illustration

def postprocess(data):
    # Handle processing of TensorFlow Serving responses
    # Simplified example, assuming 'predictions' key contains the desired data
    return data['predictions'][0]




