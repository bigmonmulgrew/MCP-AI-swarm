from datetime import datetime, timezone
from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, CAM_DATA, LOCAL_DATA

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")

            normalized_camera_data = [
                {"timestamp": ts, "cam1": c1, "cam2": c2}
                for ts, c1, c2 in CAM_DATA
            ]
            
            payload = Message(
                role = "bot"   ,                            # Message sender type
                Msg = "Structured \{\{I1}} Data",           # The actual message  # {{I1}} token for image replacement example only, no defined format yet
                Images= ["dsadas"],
                structuredMsg =  [normalized_camera_data],  # Structured data strings
                Files = [],
                Videos = []
            )
            return payload