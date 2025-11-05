from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
from time import time, sleep
import threading
import requests
import os

START_TIME = time()

# Get MCPS config from .env
MCPS_HOST = os.getenv("MCPS_HOST", "localhost")
MCPS_PORT = os.getenv("MCPS_PORT_I", 8080)

# Build full URL for the MCPS /online endpoint
MCPS_ONLINE_URL = f"http://{MCPS_HOST}:{MCPS_PORT}/online"

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

# === Background registration task ===
def announce_to_mcps():
    """
    Wait 10 seconds after startup, then send a DroneOnlineObject
    to the MCPS /online endpoint.
    """
    sleep(10)

    drone_info = DroneOnlineObject(
        ToolServerName="MCP Data server",
        ToolServerAddress=os.getenv("MCP_DATA_HOST", "mvp-data"),
        ToolServerPort=os.getenv("MCP_DATA_PORT_E", "8060"),
        ToolServerCategory="Unstructured",
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
    print("[MCO] Starting Data drone server...")
    threading.Thread(target=announce_to_mcps, daemon=True).start()