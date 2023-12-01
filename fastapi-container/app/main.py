from fastapi import FastAPI

app = FastAPI()

def some_function():
    return "Hello World"

@app.get("/")
def root():
    result = some_function()
    return {"message": result}
