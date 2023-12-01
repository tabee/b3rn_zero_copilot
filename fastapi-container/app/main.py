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
    result = some_function()
    return {"message": result}

@app.get("/call-langchain")
async def call_langchain():
    try:
        response = await http_client.get("http://langchain:80/langchain")
        return response.json()
    except httpx.RequestError as exc:
        print(f"Anfrage fehlgeschlagen: {exc}")
        # Fehlerbehandlung, wenn die Anfrage fehlschlägt
        return JSONResponse(status_code=500, content={"message": "Langchain-Service ist nicht erreichbar"})
