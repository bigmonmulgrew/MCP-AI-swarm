from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
from time import time
import requests
import os
import bootstrap

START_TIME = time()

# Get MCP-Data URL from environment variable
MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")

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
    
    # Make a POST request to MCP-Data
    try:
        response = requests.post(
            f"{MCP_DATA_URL}/query",
            json=dqo.dict(),
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data_response = response.json()
        print(f"MCP-Data response: {data_response}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling MCP-Data: {e}")
        data_response = None
    
    return {
        "msg": "Created a graph and processed the request successfully.",
        "images": [bootstrap.IMAGE],
        "files": [],
        "videos": []
    }

@app.get("/status")
async def status():
    """
    Simple health/status endpoint for the visualiser.
    """
    return {"status": "ok", "uptime_seconds": time() - START_TIME}