from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
from time import time

START_TIME = time()

# === Define the Drone Query Object (DQO) ===
class DroneQueryObject(BaseModel):
    Query: str
    RecursionDepth: int
    OriginalSPrompt: str
    MessageHistory: Dict[str, Any]
    CurrentTime: float

# === Create the API app ===
app = FastAPI(title="MCO Orchestration Server MVP")

# === Simple query endpoint ===
@app.post("/query")
async def handle_query(dqo: DroneQueryObject):
    """
    Accepts a Drone Query Object (DQO) and returns a predefined string.
    This is a stub for the orchestration server.
    """
    print(f"Received query: {dqo.Query}")
    response_text = (
        "Processed request successfully. "
        f"Received Query='{dqo.Query}' with recursion depth {dqo.RecursionDepth}."
    )
    return {
        "msg": "Returned some data successfully.",
        "images": [],
        "files": [],
        "videos": []
    }

@app.get("/status")
async def status():
    """
    Simple health/status endpoint for the visualiser.
    """
    return {"status": "ok", "uptime_seconds": time() - START_TIME}