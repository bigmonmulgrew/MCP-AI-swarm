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
                    model='qwen3-vl',
                    messages=[{
                        'role': 'system',
                        'content': '''Extract the contract start date and end date from this maintenance contract paragraph. 
                        Return ONLY a JSON object in this exact format with no other text:
                        {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}''',
                    },
                    {
                        'role': 'user',
                        'content': '''CAMERA MAINTENANCE AGREEMENT
This Camera Maintenance Agreement (“Agreement”) is made on 18 November 2025
(“Effective Date”) between:
• Greenfield Office Park Ltd, a company registered in England and Wales
(Company No. 09234567) with its registered office at 12 Greenfield Way,
Birmingham, B1 2AB, United Kingdom (“Client”); and
• Guardian Cameras & Security Ltd, a company registered in England and Wales
(Company No. 08123456) with its registered office at 48 High Street,
Manchester, M1 3CD, United Kingdom (“Service Provider”).
Client and Service Provider may be referred to individually as a “Party” and collectively
as the “Parties.”
1. TERM OF AGREEMENT
1.1 Start and End Date
This Agreement shall commence on 1 December 2025 (“Start Date”) and shall
continue in effect until 30 November 2026 (“End Date”), unless terminated earlier in
accordance with this Agreement.
1.2 Renewal
No later than 60 days before the End Date, the Parties may agree in writing to renew this
Agreement for a further period of 12 months on mutually agreed terms.
2. SCOPE OF SERVICES
2.1 Covered Equipment
Service Provider shall provide maintenance services for the following camera and
related systems installed at Greenfield Office Park, 12 Greenfield Way, Birmingham,
B1 2AB (the “Premises”):
• 24 × Fixed dome CCTV cameras (1080p HD) – Model: GC-DOME1080
• 8 × PTZ (Pan-Tilt-Zoom) cameras (4MP) – Model: GC-PTZ4M
• 2 × Network Video Recorders (NVR) – Model: GC-NVR32 (32-channel)
• Associated PoE network switches, power supplies, wall brackets, junction boxes,
and cabling.
A detailed Equipment List, including serial numbers and locations, is set out in
Schedule 1 (Equipment List).
2.2 Preventive Maintenance
Service Provider shall carry out quarterly preventive maintenance visits (4 visits per
year) during the Term, which shall include:
a. Visual inspection of all cameras, housings, mounts, and brackets
b. Cleaning of camera lenses and housings
c. Checking and tightening of fixings, mounts, and brackets
d. Verification of camera focus, alignment, and fields of view
e. Testing of infrared (IR) function on applicable cameras
f. Checking power supply units, PoE switches, and visible cabling
g. Verification that all cameras are recording correctly on the NVRs
h. Spot checks of recording playback (random time samples)
i. Confirming recording retention period is at least 30 days as agreed
j. Checking for manufacturer firmware updates and applying them where appropriate
and approved by Client.
2.3 Corrective Maintenance
In the event of a fault or malfunction of the Equipment, Service Provider shall:
a. Provide remote diagnostic support during Service Hours;
b. Attend the Premises, where necessary, to repair or replace faulty parts;
c. Restore the system to proper operating condition as soon as reasonably practicable,
subject to parts availability and site access.
2.4 Exclusions
The Services do not include:
• Repair of damage caused by vandalism, theft, fire, flood, lightning, power surges,
or other force majeure events
• Repair of damage caused by misuse, negligence, or unauthorised modification
by Client or any third party
• Relocation, redesign, or expansion of the system (e.g., adding new cameras or
cabling routes)
• Provision of monitoring centre services or internet connectivity
• Replacement of NVR hard drives due to capacity upgrades requested by Client
(as opposed to genuine failure).
Any such excluded work may be carried out under a separate quotation and agreement.
''',
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