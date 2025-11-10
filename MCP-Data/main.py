# data/main.py
from fastapi import FastAPI
from common import DroneQueryObject, BaseDroneServer

drone = BaseDroneServer(
    name="MCP Data server",
    category="Unstructured",
    env_host_key="MCP_DATA_HOST",
    env_port_key="MCP_DATA_PORT_E"
)
app = drone.app

@app.post("/query")
async def handle_query(dqo: DroneQueryObject):
    print(f"Received query: {dqo.Query}")
    return {
        "msg": "Returned some data successfully.",
        "images": [],
        "files": [],
        "videos": []
    }
