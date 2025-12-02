from fastapi import FastAPI
from common import DroneOnlineObject, DroneQueryObject, UserQuery   # Used items from common
from common import BOOT_MCPS_ONLINE_RESPONSE as ONLINE_RESPONSE                        # Bootstrapping placeholders to be removes
import requests
import os
from time import time

app = FastAPI(title="Multi Cotext Protocol Server API is runnning")

# AI queue connection info
AI_QUEUE_URL = os.getenv("AI_QUEUE_URL", "http://ai-queue:9090")

# === Environment variables === TODO temporary
MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")
MCP_VISUALISER_URL = os.getenv("MCP_VISUALISER_URL", "http://mcp-visualiser:8070")
MCP_VERDICT_URL = os.getenv("MCP_VERDICT_URL", "http://mcp-verdict:8050")

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
    return ONLINE_RESPONSE

@app.get("/offline")
def setOffline():
    return {"status: not implemented"}

@app.get("/heartbeat")
def heartbeatResponse():
    return {"status": "ok"}

@app.post("/query")
def process_user_query(data: UserQuery):
    """Endpoint for the user query or a hard coded system query.
    e.g. What are my risks?"""
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

@app.post("/ai-query")
def process_ai_query(data: dict):
    """
    Explicit endpoint for intentional AI requests.
    """
    try:
        res = requests.post(f"{AI_QUEUE_URL}/query", json=data)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        return {"error": "AI queue unreachable", "details": str(e)}


# TODO debugging only after here. Used in dev and planned ot be removed
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
    structured_msgs = []
    images = []

    # === Call Data MCP ===
    try:
        print(f"[MCPS] Calling Data MCP: {MCP_DATA_URL}/query")
        res_data = requests.post(f"{MCP_DATA_URL}/query", json=dqo.model_dump(mode = "json"))
        res_data.raise_for_status()
        data_json = res_data.json()
        msg = data_json.get("Msg", msg)
        structured_msgs = data_json.get("stucturedMsg", [])
        print(f"[MCPS] Data MCP responded with msg: {msg}")
    except requests.exceptions.RequestException as e:
        print(f"[MCPS] Error calling Data MCP: {e}")

    # === Call Visualiser MCP ===
    try:
        print(f"[MCPS] Calling Visualiser MCP: {MCP_VISUALISER_URL}/query")
        res_vis = requests.post(f"{MCP_VISUALISER_URL}/query", json=dqo.model_dump(mode = "json"))
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
                "structured_messages": structured_msgs,
                "images": images,
                "files": [],
                "videos": []
            }
        ],
    }

    return response_data

@app.post("/debug-verdict")
def debug_verdict(data: UserQuery):
    """Debug endpoint to simulate verdict processing."""
    dqo = DroneQueryObject(
        Query=data.query,
        RecursionDepth=1,
        OriginalSPrompt="You are a helpful AI assistant.",
        MessageHistory={},
        CurrentTime=time(),
    )

    try:
        print(f"[MCPS] Calling Data MCP: {MCP_DATA_URL}/query")
        res_data = requests.post(f"{MCP_DATA_URL}/query", json=dqo.model_dump(mode = "json"))
        res_data.raise_for_status()
        data_json = res_data.json()

        # Inject response back into dqo for further processing
        dqo.MessageHistory = {
            "data_drone_response": data_json["structuredMsg"]
        }
    except requests.exceptions.RequestException as e:
        print(f"[MCPS] Error calling Data MCP: {e}")

    try:
        print(f"[MCPS] Calling Verdict Drone: {MCP_VERDICT_URL}/query")
        res_verdict = requests.post(f"{MCP_VERDICT_URL}/query", json=dqo.model_dump(mode = "json"))
        res_verdict.raise_for_status()
        verdict_json = res_verdict.json()
        return verdict_json
    except requests.exceptions.RequestException as e:
        print(f"[MCPS] Error calling Verdict Drone: {e}")
        return {"error": "Verdict Drone unreachable"}
        
    