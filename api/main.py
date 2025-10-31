from fastapi import FastAPI

app = FastAPI(title="MCO Controller API")

@app.get("/")
def read_root():
    return {"message": "MCO Controller API is running"}

@app.get("/status")
def status():
    return {"status": "ok"}