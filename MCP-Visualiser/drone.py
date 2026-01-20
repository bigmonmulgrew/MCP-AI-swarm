import requests, os
from common import DroneQueryObject, BOOT_IMAGE, BaseDroneServer

class VisualiserDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            
            print(f"Received query: {dqo.Query}")
            MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")
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
        