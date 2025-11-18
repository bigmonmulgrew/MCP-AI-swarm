from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, camera_data, local_data

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")
            
            payload = Message(
                role = "bot"   ,        # Message sender type
                Msg = "Structured Data",            # Tha actual message
                stucturedMsg =  [camera_data, local_data], # Structured data strings
                Images = [],
                Files = [],
                Videos = []
            )
            return payload