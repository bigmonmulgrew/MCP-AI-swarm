from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, CAM_DATA, LOCAL_DATA

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")
            
            payload = Message(
                role = "bot"   ,                            # Message sender type
                Msg = "Structured \{\{I1}} Data",           # The actual message  # {{I1}} token for image replacement example only, no defined format yet
                Images= ["dsadas"],
                structuredMsg =  [CAM_DATA, LOCAL_DATA],  # Structured data strings
                Files = [],
                Videos = []
            )
            return payload