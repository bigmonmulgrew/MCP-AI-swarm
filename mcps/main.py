from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

class DroneQueryObject(BaseModel):
    Query: str
    RecursionDepth: int
    OriginalSPrompt: str
    MessageHistory: Dict[str, Any]
    CurrentTime: float


app = FastAPI(title="Multi Cotext Protocole Server API is runnning")

@app.get("/")
def read_root():
    return {"message": "Multi Cotext Protocole Server API is running"}

@app.get("/status")
def status():
    return {"status": "ok"}