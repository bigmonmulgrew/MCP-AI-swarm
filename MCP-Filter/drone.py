import json
from time import time
from common import DroneQueryObject, BaseDroneServer, Message, DOMAIN_JSON, parse_structured_msg
from datetime import datetime, timezone
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

            # MCP_DATA_URL = os.getenv("MCP_DATA_URL", "http://mcp-data:8060")

            # data_dqo = DroneQueryObject(
            #     Query = "Provide the data",
            #     RecursionDepth = 1,
            #     OriginalSPrompt = "You are a helpful AI assistant.",
            #     MessageHistory = dqo.MessageHistory,
            #     CurrentTime = time(),
            # )

            # data_json = None

            # try:
            #     res = requests.post(f"{MCP_DATA_URL}/query", json=data_dqo.model_dump(mode = "json"))
            #     res.raise_for_status()
            #     print(f"MCP-Data response: {res.json()}")
            #     data_json = res.json()
            # except requests.exceptions.RequestException as e:
            #     print(f"Error calling MCP-Data: {e}")

            epoch_times = []

            for item in dqo.MessageHistory["domain_drone_response"].structuredMsg[0]["timestamp"].values():
                date_time = item.split("-")
                dt = datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]), tzinfo=timezone.utc)
                epoch_time = dt.timestamp()
                epoch_times.append(epoch_time)


            print(f"Epoch times: {epoch_times}")
            apply_plan_definition = """def apply_plan(rows: List[Row], plan: Dict[str, Any]) -> List[Row]:
                                    # Define comparison operators
                                    def op_eq(val, target): 
                                        return val == target
                                    
                                    def op_ne(val, target): 
                                        return val != target
                                    
                                    def op_gt(val, target): 
                                        return val > target
                                    
                                    def op_gte(val, target): 
                                        return val >= target
                                    
                                    def op_lt(val, target): 
                                        return val < target
                                    
                                    def op_lte(val, target): 
                                        return val <= target

                                    # Map operator names to functions
                                    op_map: Dict[str, Callable[[Any, Any], bool]] = {
                                        "eq": op_eq, 
                                        "ne": op_ne, 
                                        "gt": op_gt, 
                                        "gte": op_gte, 
                                        "lt": op_lt, 
                                        "lte": op_lte
                                    }

                                    def match_all(row: Row, conditions: List[Dict[str, Any]]) -> bool:
                                        return all(
                                            op_map[c["op"]](row.get(c["field"]), c["value"]) 
                                            for c in conditions
                                        )

                                    # Start with all rows
                                    filtered = rows
                                    
                                    # Apply each filter in sequence
                                    for f in plan.get("filters", []):
                                        ftype = f.get("type")
                                        
                                        if ftype == "exclude_window":
                                            # Exclude rows whose field value falls within [start, end]
                                            start = f["start"]
                                            end = f["end"]
                                            field = f["field"]
                                            filtered = [
                                                r for r in filtered 
                                                if not (start <= r.get(field, 0) <= end)
                                            ]
                                        
                                        elif ftype == "all":
                                            # Keep only rows where all conditions are true
                                            conditions = f.get("conditions", [])
                                            filtered = [
                                                r for r in filtered 
                                                if match_all(r, conditions)
                                            ]
                                        
                                        elif ftype == "any":
                                            # Keep rows where at least one condition is true
                                            conditions = f.get("conditions", [])
                                            filtered = [
                                                r for r in filtered 
                                                if any(match_all(r, [c]) for c in conditions)
                                            ]
                                        
                                        else:
                                            raise ValueError(f"Unknown filter type: {ftype}")
                                    
                                    return filtered"""

            ai_payload_red = {
                "prompt": f"Create a JSON FilterPlan for: Flag any record where both cameras are off. This is the red filter (still just start the json with 'filters':). Here is the camera data for the filter: {dqo.MessageHistory['data_drone_response'].structuredMsg[0]}\n Output JSON only. The filter plan needs to work for the apply_plan function, which has the following function definition: {apply_plan_definition}.",
                "model": "qwen2.5-coder:7b",
                "options": {}
            }

            ai_payload_amber = {
                "prompt": f"Create a JSON FilterPlan for: Identify records outside the maintenance period, timestamp defined as start={epoch_times[0]} and end={epoch_times[-1]}. This is the amber filter (still just start the json with 'filters':). The filter plan needs to work for the apply_plan function, which has the following function definition: {apply_plan_definition}. Output JSON only.",
                "model": "qwen2.5-coder:7b",
                "options": {}
            }
            structured_data = []

            retry_count = 0
            red_respone_parsed = False
            amber_response_parsed = False
            json_response_red = None
            json_response_amber = None
            while retry_count < 3 and (not red_respone_parsed or not amber_response_parsed):
                
                if not red_respone_parsed:
                    try:
                        response = requests.post(API_URL, json=ai_payload_red, timeout = 120)
                        response.raise_for_status()
                        json_response_red = response.json()
                    except Exception as e:
                        print(e)

                if not amber_response_parsed:
                    try:
                        response = requests.post(API_URL, json=ai_payload_amber, timeout = 120)
                        response.raise_for_status()
                        json_response_amber = response.json()
                    except Exception as e:
                        print(e)

                print(f"AI response (red): {json_response_red['result']['response']}")
                print(f"AI response (amber): {json_response_amber['result']['response']}")

            
                # Handle case where request failed
                if json_response_red is None or 'result' not in json_response_red:
                    structured_data += []
                else:
                    try:
                        structured_data.append(parse_structured_msg([json_response_red['result']['response']]))
                        red_respone_parsed = True
                    except Exception as e:
                        retry_count += 1

                if json_response_amber is  None and 'result' not in json_response_amber:
                    structured_data += []
                else:
                    try:
                        structured_data.append(parse_structured_msg([json_response_amber['result']['response']]))
                        amber_response_parsed = True
                    except Exception as e:
                        retry_count += 1
            
            payload = Message(
                role="bot",
                Msg="Response from FilterDrone",
                Images=[],
                structuredMsg=structured_data,
                Files=[],
                Videos=[]
            )

            print(payload)
            return payload
    
    # Add custom methods below
    # def custom_method(self):
    #     pass
