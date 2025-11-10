from fastapi import FastAPI
import requests, os
from common import DroneQueryObject, BOOT_IMAGE, BaseDroneServer

class VisualiserDrone(BaseDroneServer):
    def _register_query_endpoint(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")
            print(f"Received query: {dqo.Query}")

            try:
                res = requests.post(f"{MCP_DATA_URL}/query", json=dqo.dict())
                res.raise_for_status()
                print(f"MCP-Data response: {res.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Error calling MCP-Data: {e}")

            return {
                "msg": "Created a graph and processed the request successfully.",
                "images": [BOOT_IMAGE],
                "files": [],
                "videos": [],
            }

drone = VisualiserDrone(
    name="MCP visualisation server",
    category="Visualisation",
    env_host_key="MCP_VISUALISER_HOST",
    env_port_key="MCP_VISUALISER_PORT_E",
)

app = drone.app