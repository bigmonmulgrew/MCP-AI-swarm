from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
from time import time, sleep
import requests
import os
import threading
import bootstrap

START_TIME = time()

# Get MCPS config from .env
MCPS_HOST = os.getenv("MCPS_HOST", "localhost")
MCPS_PORT = os.getenv("MCPS_PORT_I", 8080)

# Build full URL for the MCPS /online endpoint
MCPS_ONLINE_URL = f"http://{MCPS_HOST}:{MCPS_PORT}/online"

# Get MCP-Data URL from environment variable
MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")

# === Define the Drone Query Object (DQO) ===
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
    Timeout:int

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

# === Background registration task ===
def announce_to_mcps():
    """
    Wait 10 seconds after startup, then send a DroneOnlineObject
    to the MCPS /online endpoint.
    """
    sleep(10)

    drone_info = DroneOnlineObject(
        ToolServerName="MCP visualisation server",
        ToolServerAddress=os.getenv("MCP_VISUALISER_HOST", "mvp-visualiser"),
        ToolServerPort=os.getenv("MCP_VISUALISER_PORT_E", "8050"),
        ToolServerCategory="Visualisation",
        Timeout=300
    )

    print(f"[MCO] Sending online registration to {MCPS_ONLINE_URL}...", flush=True)
    try:
        res = requests.post(MCPS_ONLINE_URL, json=drone_info.model_dump())
        res.raise_for_status()
        print(f"[MCO] Successfully registered with MCPS: {res.json()}", flush=True)
    except requests.exceptions.RequestException as e:
        print(f"[MCO] Failed to register with MCPS: {e}", flush=True)

@app.on_event("startup")
def startup_event():
    """Runs when FastAPI starts."""
    print("[MCO] Starting Visualiser drone server...")
    threading.Thread(target=announce_to_mcps, daemon=True).start()