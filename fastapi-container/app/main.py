from fastapi import FastAPI
import httpx
from starlette.responses import JSONResponse

app = FastAPI()

# Eine Instanz des HTTP-Clients erstellen
http_client = httpx.AsyncClient()

def some_function():
    return "Hello World"

@app.get("/")
def root():
    return {"message": some_function()}

@app.get("/call-langchain")
async def call_langchain():
    try:
        response = await http_client.get("http://langchain:8000")
        return response.json()
    except httpx.RequestError as exc:
        print(f"Anfrage fehlgeschlagen: {exc}")
        # Fehlerbehandlung, wenn die Anfrage fehlschlägt
        return JSONResponse(status_code=500, content={"message": "Langchain-Service ist nicht erreichbar"})

@app.get("/joke/{topic}")
async def call_langchain(topic: str):
    try:
        response = await http_client.get(f"http://langchain:8000/joke/{topic}")
        return response.json()
    except httpx.RequestError as exc:
        print(f"Anfrage fehlgeschlagen: {exc}")
        # Fehlerbehandlung, wenn die Anfrage fehlschlägt
        return JSONResponse(status_code=500, content={"message": "Langchain-Service ist nicht erreichbar"})