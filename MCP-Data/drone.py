from datetime import datetime, timezone
from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, CAM_DATA, LOCAL_DATA

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")

            epoch_times = []

            for item in LOCAL_DATA.values():
                date_time = item.split("-")
                dt = datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]), tzinfo=timezone.utc)
                epoch_time = dt.timestamp()
                epoch_times.append(epoch_time)
            

            #epoch_time = datetime()

            
            # epoch_time = dt.timestamp()
            # print(epoch_time)
            
            payload = Message(
                role = "bot"   ,                            # Message sender type
                Msg = "Structured \{\{I1}} Data",           # The actual message  # {{I1}} token for image replacement example only, no defined format yet
                Images= ["dsadas"],
                structuredMsg =  [CAM_DATA, epoch_times],  # Structured data strings
                Files = [],
                Videos = []
            )
            return payload