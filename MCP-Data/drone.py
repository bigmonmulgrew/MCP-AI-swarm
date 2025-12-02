from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, camera_data, local_data

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")
            
            payload = Message(
                role = "bot"   ,                            # Message sender type
                Msg = "Structured \{\{I1}} Data",           # The actual message  # {{I1}} token for image replacement example only, no defined format yet
                Images= ["dsadas"],
                stucturedMsg =  [camera_data, local_data],  # Structured data strings
                Files = [],
                Videos = []
            )
            return payload