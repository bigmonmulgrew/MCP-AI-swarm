from common import DroneQueryObject, BaseDroneServer, Message

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")
            
            payload = Message(
                role = "bot"   ,        # Message sender type
                Msg = "Structured Data",            # Tha actual message
                stucturedMsg =  {"dsadsa", "dsadsa" }# Structured data strings
            )
            return payload