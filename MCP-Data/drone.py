from datetime import datetime, timedelta, timezone
import json
import os

import requests
from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, CAM_DATA, LOCAL_DATA

TOKEN = os.getenv("BLOC_TOKEN", None)
ENDPOINT = os.getenv("BLOC_ENDPOINT", None)
DATA_ID = os.getenv("BLOC_DATA_ID", None)

last_query_time = None

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")

            global last_query_time
            # Use global last_query_time to track the last time data was queried
            if not last_query_time:
                last_query_time = datetime.now(timezone.utc) - timedelta(minutes=10)  # Default to last 10 minutes
                last_query_time = last_query_time.timestamp() * 1000  # Convert to milliseconds

            url = ENDPOINT

            print(f"Querying data from {last_query_time} to {datetime.now(timezone.utc).timestamp()}")
            payload = json.dumps({
            "id": DATA_ID,
            "variables": [
                "696e0f62ee627309bd87b5a2",
                "696e0f62ee627309bd87b5a0",
                "696e0f62ee627309bd87b5a1"
            ],
            "indexFilter": {
                "mode": "between",
                "value": [
                last_query_time,
                datetime.now(timezone.utc).timestamp()
                ]
            }
            })
            headers = {
            'token': TOKEN,
            'Content-Type': 'application/json'
            }
            
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
            except Exception as error:
                print(f"Error during request: {error}")
                return Message(
                    role="bot",
                    Msg="Error retrieving camera data.",
                    Images=[],
                    structuredMsg=[],
                    Files=[],
                    Videos=[]
                )
            
            cam_data = response.json()
            source = cam_data["source"]

            normalized_camera_data = [
                # {"timestamp": ts, "cam1": c1, "cam2": c2}
                # for ts, c1, c2 in CAM_DATA
                {"timestamp": ts, "cam1": c1, "cam2": c2}
                for ts, c1, c2 in source
            ]
            
            payload = Message(
                role = "bot"   ,                            # Message sender type
                Msg = "Here is the camera data",           # The actual message  # {{I1}} token for image replacement example only, no defined format yet
                Images= [],
                structuredMsg =  [normalized_camera_data],  # Structured data strings
                Files = [],
                Videos = []
            )

            # Update last query time
            last_query_time = datetime.now(timezone.utc).timestamp()
            return payload