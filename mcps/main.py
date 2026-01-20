import logging
import json
from common import setup_logging

from fastapi import FastAPI, HTTPException
from common import DroneOnlineObject, DroneQueryObject, UserQuery, BlocHubResponse, AIQuery   # Used items from common
from common import BOOT_MCPS_ONLINE_RESPONSE as ONLINE_RESPONSE                        # Bootstrapping placeholders to be removes
from common import BOOT_BLOC_HUB_RESPONSE, BOOT_QUERY_RESPOSNE_01, BOOT_SYSTEM_QUERY
from common import CAM_DATA
from cam_test import analyse_camera_data
import requests
import os
from time import time

app = FastAPI(title="Multi Cotext Protocol Server API is runnning")

LOG_LEVEL="INFO"    # Valid levels CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

logger = logging.getLogger(__name__)
setup_logging(LOG_LEVEL)

logger.info("Starting Orcestration server (MCPS)")

# AI queue connection info
AI_QUEUE_URL = os.getenv("AI_QUEUE_URL", "http://ai-queue:9090")

# Ollama settings
OLLAMA_MODEL: str = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")
OLLAMA_TEMP: float = os.getenv("OLLAMA_DEFAULT_TEMP", 0.0)
OLLAMA_MAX_TOKENS: int = os.getenv("OLLAMA_MAX_TOKENS", 10000)
OLLAMA_TIMEOUT: int = os.getenv("OLLAMA_TIMEOUT", 300)

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

    return BOOT_QUERY_RESPOSNE_01

@app.get("/bloc-query")
def process_bloc_query_get(verbose: bool = False):
    """Tailored endpoint for testing Bloc's use case.
    Returns a BlocHubResponse object. When verbose = true also includes reasoning data
    """
    boot_response = BlocHubResponse(**BOOT_BLOC_HUB_RESPONSE)

    system_query = BOOT_SYSTEM_QUERY
    domain_data:str = "This factory contains hazardous materials, it would be a breach of the law if the site is unmonitored"
    local_summary:str = "Monitoring will be by camera, at least one camera must be enabled. In any case where two cameras are off this would mean a serious breach and high risk.."
    camera_summary: str = analyse_camera_data(CAM_DATA)

    system_prompt: str = f"""
{system_query}

## Domain data 
This is a summary of laws, and rules relavant to this industry or process.
{domain_data}
## Domain Data Ends

## Local data
This is a collection of company policies, contract terms and local Standard Operating Procedures.
{local_summary}
## Local data Ends

## Camera Data
This is a timestamped log of the camera data, any provided camera logs have one or more cameras offline and this represents an issue. Cross reference this with the other proivided data to determine adequate limits.
{camera_summary}
## Camera summary ends
""".strip()

    logger.info("Printing full system prompt")
    logger.info(system_prompt)
    
    query_data = AIQuery(
        prompt=system_prompt,
        model=OLLAMA_MODEL,
        temperature=OLLAMA_TEMP,
        max_tokens=OLLAMA_MAX_TOKENS,
        options = {}
        
    )

    response = requests.post(
        f"{AI_QUEUE_URL}/query", 
        json=query_data.model_dump(mode="json"),
        timeout=OLLAMA_TIMEOUT
        )
    
    response.raise_for_status()
    
    queue_payload = response.json()
    
    logger.info("Printing returned payload")
    logger.info(queue_payload)
    
    model_result = queue_payload["result"]
    
    resp_text = model_result.get("response", "")
    
    try:
        model_json = json.loads(resp_text)
    except Exception as e:
        # Return a 502 with useful debug info (truncated)
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Model returned non-JSON response",
                "parse_error": str(e),
                "raw_response_prefix": resp_text[:500],
            },
        )
    
    model_json = json.loads(model_result["response"])

    logger.info("Printing cleaned JSON")
    logger.info(model_json)
    
    response_data = BlocHubResponse(
        light_result=model_json.get("score"),
        text_result=model_json.get("text_result", ""),
        time=int(time()),
    )
    
    if verbose:
        debug_data = {
            "domain_summary": domain_data,
            "local_summary": local_summary,
            "camera_summary": camera_summary
        }
        response_data.debug_data=debug_data

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