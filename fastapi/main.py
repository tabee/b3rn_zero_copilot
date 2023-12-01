from fastapi import FastAPI
import requests
import os

app = FastAPI()

langchain_url = os.getenv("LANGCHAIN_URL", "http://localhost:5000")

@app.get("/process")
def process_data():
    response = requests.get(f"{langchain_url}/process")
    return response.json()
