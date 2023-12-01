from fastapi import FastAPI
import httpx
from starlette.responses import JSONResponse

app = FastAPI()

# Eine Instanz des HTTP-Clients erstellen
http_client = httpx.AsyncClient()

def some_function():
    return "Hello Langchain"

@app.get("/langchain")
def hello_langchain():
    result = some_function()
    return {"message": result}
