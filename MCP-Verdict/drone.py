from time import timezone
from datetime import datetime
from common import DroneQueryObject, BaseDroneServer, Message, apply_plan
from pathlib import Path

class VerdictDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):

            print(f"Received query: {dqo.Query}")

            # print(dqo.MessageHistory["filter_drone_response"].structuredMsg[0].values())

            red_filter = dqo.MessageHistory["filter_drone_response"].structuredMsg[0]
            amber_filter = dqo.MessageHistory["filter_drone_response"].structuredMsg[1]

            print("Red Filter Plan:")
            print(red_filter)
            print("Amber Filter Plan:")
            print(amber_filter)

            # red_plan = {
            #     "filters": red_filter
            # }

            # amber_plan = {
            #     "filters": amber_filter
            # }

            # print(dqo.MessageHistory["filter_drone_response"].structuredMsg[0]["red_filter"])
            # print(dqo.MessageHistory["filter_drone_response"].structuredMsg[0]["amber_filter"])

            # red_filter = dqo.MessageHistory["filter_drone_response"].structuredMsg[0]["red_filter"]

            # amber_filter = dqo.MessageHistory["filter_drone_response"].structuredMsg[0]["amber_filter"]

            # Apply filter plans to camera data
            red_matches = apply_plan(dqo.MessageHistory["data_drone_response"].structuredMsg[0], red_filter)
            amber_matches = apply_plan({"timestamp": datetime.now(timezone.utc).timestamp() * 1000}, amber_filter)
            
            # Determine verdict based on matches
            # Red = critical issue (both cameras off)
            # Amber = warning (maintenance period detected)
            # Green = all clear
            if len(red_matches) > 0:
                verdict = 2
                msg = f"CRITICAL: Found {len(red_matches)} instances where both cameras were off."
            elif len(amber_matches) > 0:
                verdict = 1
                msg = f"WARNING: Found {len(amber_matches)} records outside maintenance period."
            else:
                verdict = 0
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

            print(f"I AM A VERDICT: {payload.structuredMsg['verdict']}")
            return payload