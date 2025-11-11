from common import DroneQueryObject, BaseDroneServer

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            print(f"Received query: {dqo.Query}")
            return {
                "msg": "Returned some data successfully.",
                "images": [],
                "files": [],
                "videos": [],
            }