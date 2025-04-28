from fastapi import FastAPI, HTTPException, Header, status
from typing import Dict, Optional
import time
import random
import uuid
from threading import Thread

app = FastAPI()

# Store prediction results in memory
prediction_results: Dict[str, Dict[str, str]] = {}

"""
- machine learning model prediction.
- input string for the mock model
- it will return a dictionary A dictionary containing the input and a simulated result.
- Example: {"input": "input_data", "result": "12345"}
"""
def mock_model_predict(input: str) -> Dict[str, str]:
    time.sleep(random.randint(10, 17))  
    result = str(random.randint(1000, 20000))  
    output = {"input": input, "result": result}  
    return output

"""
- mock model prediction asynchronously and stores the result.
- prediction_id = unique ID for this prediction.
- input string for the mock model
- This function does not return a value.  It updates the 'prediction_results' dictionary.
"""
def process_prediction_async(prediction_id: str, input_data: str):
    result = mock_model_predict(input_data)
    prediction_results[prediction_id] = {"status": "completed", "output": result}

"""
- Handles both synchronous and asynchronous prediction requests.
- If the Async-Mode header is "true", the request is processed asynchronously.
- Otherwise, it is processed synchronously.
- Returns either the prediction result (synchronous) or a message with the prediction ID (asynchronous).
    Returns a 202 status code if the request is asynchronous.
- Possible return structures:
    - Synchronous: {"input": "input_data", "result": "12345"}
    - Asynchronous: {"message": "Request received...", "prediction_id": "some_uuid"}
- Raises HTTPException: 400 if the input is missing.
"""
@app.post("/predict")
async def predict(
    input_data: Dict[str, str],
    async_mode: Optional[str] = Header(None, alias="Async-Mode")
):
    input_string = input_data.get("input")  
    if input_string is None:
        raise HTTPException(status_code=400, detail="Input is required")  

    if async_mode == "true": 
        prediction_id = str(uuid.uuid4()) 
        prediction_results[prediction_id] = {"status": "processing"} 

        thread = Thread(target=process_prediction_async, args=(prediction_id, input_string))
        thread.start()

        return {
            "message": "Request received. Processing asynchronously.",  
            "prediction_id": prediction_id  
        }, status.HTTP_202_ACCEPTED  
    else:
        prediction_result = mock_model_predict(input_string)  
        return prediction_result  

"""
- Retrieves the result of an asynchronous prediction.
- prediction_id = unique ID of the prediction to retrieve.
- Returns the prediction result, including the prediction ID and output.
    Example: {"prediction_id": "some_uuid", "output": {"input": "...", "result": "..."}}
- Raises HTTPException: 404 if the prediction ID is not found.
- Raises HTTPException: 400 if the prediction is still being processed.
"""
@app.get("/predict/{prediction_id}")
async def get_prediction_result(prediction_id: str):
    if prediction_id not in prediction_results:
        raise HTTPException(status_code=404, detail="Prediction ID not found.")  

    result = prediction_results[prediction_id]

    if result["status"] == "processing":
        raise HTTPException(status_code=400, detail="Prediction is still being processed.")  

    return {"prediction_id": prediction_id, "output": result["output"]}  


# How to run:
# Run: uvicorn main:app --reload --port 8080

# Example curl commands:
# open cmd and run these curl commands for sync and async 
# Synchronous:
# curl -X POST -H "Content-Type: application/json" -d '{"input": "Sync input my name is sania"}' http://localhost:8080/predict  
# Asynchronous:
# curl -X POST -H "Content-Type: application/json" -H "Async-Mode: true" -d '{"input": "Async input my name is sania"}' http://localhost:8080/predict  
# Get result:
# curl http://localhost:8080/predict/{prediction_id} 