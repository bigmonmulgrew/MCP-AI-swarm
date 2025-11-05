from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

class DroneQueryObject(BaseModel):
    Query: str
    RecursionDepth: int
    OriginalSPrompt: str
    MessageHistory: Dict[str, Any]
    CurrentTime: float

class DroneOnlineObject(BaseModel):
    ToolServerName: str
    ToolServerAddress: str
    ToolServerPort: str
    ToolServerCategory: str
    Timeout:300

app = FastAPI(title="Multi Cotext Protocol Server API is runnning")

@app.get("/")
def read_root():
    return {"message": "Multi Cotext Protocol Server API is running"}

@app.get("/status")
def status():
    return {"status": "ok"}

@app.get("/online")
def setOnline():
    return {"status": "ok"}

@app.get("/offline")
def setOffline():
    return {"status: not implemented"}

@app.get("/heartbeat")
def heartbeatResponse():
    return {"status": "ok"}