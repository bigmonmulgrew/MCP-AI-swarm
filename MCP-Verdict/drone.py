from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, T_LIGHT_RULES
from pathlib import Path

class VerdictDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):

            print(f"Received query: {dqo.Query}")
            
            payload = Message(
                role = "bot"   ,                            # Message sender type
                Msg = "",           # The actual message  # {{I1}} token for image replacement example only, no defined format yet
                structuredMsg =  [T_LIGHT_RULES],  # Structured data strings
                Images = [],
                Files = [],
                Videos = []
            )
            return payload