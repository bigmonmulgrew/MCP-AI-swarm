from fastapi import FastAPI
from mco_common.structs import DroneOnlineObject, DroneQueryObject, UserQuery

app = FastAPI(title="Multi Cotext Protocol Server API is runnning")

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