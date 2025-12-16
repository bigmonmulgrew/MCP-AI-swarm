from common import DroneQueryObject, BaseDroneServer, Message

class DomainDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):
            """
            Handle incoming query requests.
            
            Args:
                dqo: DroneQueryObject containing the query data
                
            Returns:
                Message: Response message with processed data
            """
            print(f"Received query: {dqo.Query}")
            
            # TODO: Implement your query handling logic here
            # Example: Process the query and return structured data
            
            payload = Message(
                role="bot",
                Msg="Response from DomainDrone",
                Images=[],
                structuredMsg=[],
                Files=[],
                Videos=[]
            )
            return payload
    
    # Add custom methods below
    # def custom_method(self):
    #     pass
