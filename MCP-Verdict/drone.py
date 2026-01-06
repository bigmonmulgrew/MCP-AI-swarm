from common import (
    DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, 
    apply_plan, red_plan, amber_plan, normalized_camera_data
)
from pathlib import Path

class VerdictDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):

            print(f"Received query: {dqo.Query}")

            # Apply filter plans to camera data
            red_matches = apply_plan(dqo.MessageHistory["data_drone_response"].structuredMsg[0], dqo.MessageHistory["filter_drone_response"].structuredMsg[0]["red_filter"])
            amber_matches = apply_plan(dqo.MessageHistory["data_drone_response"].structuredMsg[0], dqo.MessageHistory["filter_drone_response"].structuredMsg[0]["amber_filter"])
            
            # Determine verdict based on matches
            # Red = critical issue (both cameras off)
            # Amber = warning (maintenance period detected)
            # Green = all clear
            if len(red_matches) > 0:
                verdict = "red"
                msg = f"CRITICAL: Found {len(red_matches)} instances where both cameras were off."
            elif len(amber_matches) > 0:
                verdict = "amber"
                msg = f"WARNING: Found {len(amber_matches)} records outside maintenance period."
            else:
                verdict = "green"
                msg = "All clear: No issues detected."
            
            payload = Message(
                role = "bot",
                Msg = msg,
                structuredMsg = {
                    "verdict": verdict,
                    "red_matches": len(red_matches),
                    "amber_matches": len(amber_matches),
                    "red_data": red_matches,
                    "amber_data": amber_matches
                },
                Images = [],
                Files = [],
                Videos = []
            )
            return payload