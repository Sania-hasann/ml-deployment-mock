# ZypherAI Prediction App

This is a **FastAPI** web application developed as part of a **Software Development Engineer (SDE) Interview Assessment**.  
It simulates machine learning model predictions through a mock function and provides both synchronous and asynchronous prediction endpoints.

## Features

- **/predict (POST)**: Accepts an input string and returns a simulated prediction.
  - Supports **synchronous** and **asynchronous** prediction modes.
- **/predict/{prediction_id} (GET)**: Retrieves the result of an asynchronous prediction.
- **Error Handling**: Proper status codes and error messages for invalid inputs and unavailable predictions.
- **Dockerized**: Easily deployable using the included Dockerfile.

## Tech Stack

- Python 3.x
- FastAPI
- Docker

## How It Works

- **Synchronous Prediction**: Immediately returns a mock prediction based on the input.
- **Asynchronous Prediction**: Processes the prediction in the background and allows the user to fetch the result later using a prediction ID.
- **Mock Prediction**: Simulates processing delays and generates a randomized result without using real ML models.

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload
