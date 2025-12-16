import json
from time import time
from common import DroneQueryObject, BaseDroneServer, Message, DOMAIN_JSON, normalized_camera_data
import os
import requests

API_URL = "http://" + os.getenv("MCPS_HOST", "127.0.0.1") + ":" + os.getenv("MCPS_PORT", "8080") + "/ai-query"

class FilterDrone(BaseDroneServer):
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

            MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")

            data_dqo = DroneQueryObject(
                Query = "Provide the data",
                RecursionDepth = 1,
                OriginalSPrompt = "You are a helpful AI assistant.",
                MessageHistory = dqo.MessageHistory,
                CurrentTime = time(),
            )

            data_json = None

            try:
                res = requests.post(f"{MCP_DATA_URL}/query", json=data_dqo.model_dump(mode = "json"))
                res.raise_for_status()
                print(f"MCP-Data response: {res.json()}")
                data_json = res.json()
            except requests.exceptions.RequestException as e:
                print(f"Error calling MCP-Data: {e}")

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # TODO: add the apply_filter function definition to the prompt 
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ai_payload = {
                "prompt": f"Create a JSON FilterPlan for: Flag any record where both cameras are off. This is the red filter. Here is the camera data for the filter: {json.dumps(normalized_camera_data)}\n Output JSON only. Then, create a JSON FilterPlan for: Identify records outside the maintenance period, defined as start={data_json['structuredMsg'][1][0]} and end={data_json['structuredMsg'][1][1]}. This is the amber filter. Output JSON only.",
                "model": "qwen3:1.7b",
                "options": {}
            }

            print(ai_payload["prompt"])

            json_response = None
            try:
                response = requests.post(API_URL, json=ai_payload, timeout = 120)
                response.raise_for_status()
                json_response = response.json()
            except Exception as e:
                print(e)
            
            payload = Message(
                role="bot",
                Msg="Response from FilterDrone",
                Images=[],
                structuredMsg=[json_response["result"]["response"]],
                Files=[],
                Videos=[]
            )
            return payload
    
    # Add custom methods below
    # def custom_method(self):
    #     pass
