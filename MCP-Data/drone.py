from common import DroneQueryObject, BaseDroneServer, Message, BOOT_IMAGE, camera_data, local_data
import ollama
import os
from pathlib import Path

class DataDrone(BaseDroneServer):
    def _register_subclass_endpoints(self):
        @self.app.post("/query")
        async def handle_query(dqo: DroneQueryObject):

            print(f"Received query: {dqo.Query}")
            
            # Path to the PDF file
            pdf_path = Path(__file__).parent / "Maintenance Contract PDF.pdf"
            
            # Get Ollama host from environment or use default
            ollama_host = os.getenv('OLLAMA_HOST', 'ollama')
            ollama_port = os.getenv('OLLAMA_PORT_I', '11434')
            
            # Make request to Ollama to extract dates from PDF
            try:
                client = ollama.Client(host=f'http://{ollama_host}:{ollama_port}')
                
                response = client.chat(
                    model='phi4',
                    messages=[{
                        'role': 'user',
                        'content': '''Extract the contract start date and end date from this maintenance contract PDF. 
                        Return ONLY a JSON object in this exact format with no other text:
                        {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}''',
                        'images': [str(pdf_path)]
                    }],
                    format='json'
                )
                
                # Extract the dates from the response
                contract_dates = response['message']['content']
                print(f"Extracted dates: {contract_dates}")
                
            except Exception as e:
                print(f"Error calling Ollama: {e}")
                contract_dates = {"error": str(e)}
            
            payload = Message(
                role = "bot",
                Msg = "Structured {{I1}} Data with contract dates",
                stucturedMsg = [camera_data, local_data, contract_dates],
                Images = [],
                Files = [],
                Videos = []
            )
            return payload