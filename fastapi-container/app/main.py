from fastapi import FastAPI
import httpx

app = FastAPI()

def some_function():
    return "Hello World"

@app.get("/")
def root():
    result = some_function()
    return {"message": result}

@app.get("/call-langchain")
async def call_langchain():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://langchain:80/hello-langchain")
        return response.json()