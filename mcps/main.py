from fastapi import FastAPI
from mco_common.structs import DroneOnlineObject, DroneQueryObject, UserQuery
import requests
import os
from time import time

app = FastAPI(title="Multi Cotext Protocol Server API is runnning")

# === Environment variables === TODO temporary
MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")
MCP_VISUALISER_URL = os.getenv("MCP_VISUALISER_URL", "http://mcp-visualiser:8070")

@app.get("/")
def read_root():
    return {"message": "Multi Cotext Protocol Server API is running"}

@app.get("/status")
def status():
    return {"status": "ok"}

@app.post("/online")
def set_online(data: DroneOnlineObject):
    """
    Called by a drone to register itself as online.
    Example payload:
    {
        "ToolServerName": "Background Data Tool",
        "ToolServerAddress": "127.0.0.1",
        "ToolServerPort": "21010",
        "ToolServerCategory": "Unstructured Text",
        "Timeout": 300
    }
    """
    print(f"MCPS Received ONLINE notification: {data.ToolServerName}")
    # In production, you would register this drone in memory or database
    return {"status": "ok", "received": data.model_dump()}

@app.get("/offline")
def setOffline():
    return {"status: not implemented"}

@app.get("/heartbeat")
def heartbeatResponse():
    return {"status": "ok"}

@app.post("/query")
def process_user_query(data: UserQuery):
    
    response_data = {
        "status": 200,
        "query": "user asked something",
        "chat_name": "sample chat name",
        "results": [
            {
                "message": "sample message response",
                "images": [],
                "files": [],
                "videos":[]
            }
        ],
    }
    
    return response_data

@app.post("/query-stack")
def process_user_query_stack(data: UserQuery):
    """Orchestrates user queries by calling both data and visualiser drones."""
    print(f"[MCPS] Received user query: {data.query}", flush=True)

    # Build a DroneQueryObject (placeholder content for now)
    dqo = DroneQueryObject(
        Query=data.query,
        RecursionDepth=1,
        OriginalSPrompt="You are a helpful AI assistant.",
        MessageHistory={},
        CurrentTime=time(),
    )

    msg = "No response from Data Drone"
    images = []

    # === Call Data MCP ===
    try:
        print(f"[MCPS] Calling Data MCP: {MCP_DATA_URL}/query")
        res_data = requests.post(f"{MCP_DATA_URL}/query", json=dqo.model_dump())
        res_data.raise_for_status()
        data_json = res_data.json()
        msg = data_json.get("msg", msg)
        print(f"[MCPS] Data MCP responded with msg: {msg}")
    except requests.exceptions.RequestException as e:
        print(f"[MCPS] Error calling Data MCP: {e}")

    # === Call Visualiser MCP ===
    try:
        print(f"[MCPS] Calling Visualiser MCP: {MCP_VISUALISER_URL}/query")
        res_vis = requests.post(f"{MCP_VISUALISER_URL}/query", json=dqo.model_dump())
        res_vis.raise_for_status()
        vis_json = res_vis.json()
        images = vis_json.get("images", [])
        print(f"[MCPS] Visualiser MCP returned {len(images)} image(s)")
    except requests.exceptions.RequestException as e:
        print(f"[MCPS] Error calling Visualiser MCP: {e}")

    # === Combine responses ===
    response_data = {
        "status": 200,
        "query": data.query,
        "chat_name": "sample chat name",
        "results": [
            {
                "message": msg,
                "images": images,
                "files": [],
                "videos": []
            }
        ],
    }

    return response_data