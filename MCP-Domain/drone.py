import requests
from common import DroneQueryObject, BaseDroneServer, Message

API_URL = "http://localhost:9090/query"

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

            ai_payload = {
                "prompt": "tell me about lightning mcqueen",
                "model": "qwen3:1.7b",
                "options": {}
            }

            try:
                response = requests.post(API_URL, json=ai_payload, timeout = 120)
                response.raise_for_status()
                print(response.json())
            except Exception as e:
                print(e)
            
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
