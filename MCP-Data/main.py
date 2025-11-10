# data/main.py
from fastapi import FastAPI
from common import DroneQueryObject, BaseDroneServer

class DataDrone(BaseDroneServer):
    def _register_query_endpoint(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")
            return {
                "msg": "Returned some data successfully.",
                "images": [],
                "files": [],
                "videos": [],
            }

drone = DataDrone(
    name="MCP Data server",
    category="Unstructured",
    env_host_key="MCP_DATA_HOST",
    env_port_key="MCP_DATA_PORT_E",
)

app = drone.app