from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, camera_data, local_data
import os
from pathlib import Path

class VerdictDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):

            print(f"Received query: {dqo.Query}")
            
            payload = Message(
                role = "bot",
                Msg = "",
                stucturedMsg = [],
                Images = [],
                Files = [],
                Videos = []
            )
            return payload