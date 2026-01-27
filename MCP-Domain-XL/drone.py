import io
import os
import requests
import asyncio
import logging

from common import DroneQueryObject, BaseDroneServer, Message, parse_structured_msg
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from neo4j import GraphDatabase
from helpers.process_document import process_document
from helpers.chunk_text import chunk_text
from helpers.embed_text import embed_text

# environment settings
NEO4J_URI = "bolt://neo4j-db-container"
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

MCPS_API_URL = "http://" + os.getenv("MCPS_HOST", "127.0.0.1") + ":" + os.getenv("MCPS_PORT", "8080") + "/ai-query"

DOMAIN_MODEL = os.getenv("DOMAIN_MODEL", "qwen3:1.7b")

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

            json_format = """{
                "law": "All storage sites (of dangerous materials) must be constantly monitored",
                "timestamp": {
                    "start_date": "2025-12-01",
                    "end_date": "2026-11-30"
                }
            }"""

            ai_payload = {
                "prompt": f"Your task is to analyse the following domain data and provide the law and maintenance period in a JSON structured format ({json_format}):\n \nDomain Data:  Law (Rule): All storage sites (of dangerous materials) must be constantly monitored\n\nMaintenance Contract: CAMERA MAINTENANCE AGREEMENT\nThis Camera Maintenance Agreement (“Agreement”) is made on 18 November 2025\n(“Effective Date”) between:\n• Greenfield Office Park Ltd, a company registered in England and Wales\n(Company No. 09234567) with its registered office at 12 Greenfield Way,\nBirmingham, B1 2AB, United Kingdom (“Client”); and\n• Guardian Cameras & Security Ltd, a company registered in England and Wales\n(Company No. 08123456) with its registered office at 48 High Street,\nManchester, M1 3CD, United Kingdom (“Service Provider”).\nClient and Service Provider may be referred to individually as a “Party” and collectively\nas the “Parties.”\n1. TERM OF AGREEMENT\n1.1 Start and End Date\nThis Agreement shall commence on 1 December 2025 (“Start Date”) and shall\ncontinue in effect until 30 November 2026 (“End Date”), unless terminated earlier in\naccordance with this Agreement.\n1.2 Renewal\nNo later than 60 days before the End Date, the Parties may agree in writing to renew this\nAgreement for a further period of 12 months on mutually agreed terms.\n2. SCOPE OF SERVICES\n2.1 Covered Equipment\nService Provider shall provide maintenance services for the following camera and\nrelated systems installed at Greenfield Office Park, 12 Greenfield Way, Birmingham,\nB1 2AB (the “Premises”):\n• 24 × Fixed dome CCTV cameras (1080p HD) – Model: GC-DOME1080\n• 8 × PTZ (Pan-Tilt-Zoom) cameras (4MP) – Model: GC-PTZ4M\n• 2 × Network Video Recorders (NVR) – Model: GC-NVR32 (32-channel)\n• Associated PoE network switches, power supplies, wall brackets, junction boxes,\nand cabling.\nA detailed Equipment List, including serial numbers and locations, is set out in\nSchedule 1 (Equipment List).\n2.2 Preventive Maintenance\nService Provider shall carry out quarterly preventive maintenance visits (4 visits per\nyear) during the Term, which shall include:\na. Visual inspection of all cameras, housings, mounts, and brackets\nb. Cleaning of camera lenses and housings\nc. Checking and tightening of fixings, mounts, and brackets\nd. Verification of camera focus, alignment, and fields of view\ne. Testing of infrared (IR) function on applicable cameras\nf. Checking power supply units, PoE switches, and visible cabling\ng. Verification that all cameras are recording correctly on the NVRs\nh. Spot checks of recording playback (random time samples)\ni. Confirming recording retention period is at least 30 days as agreed\nj. Checking for manufacturer firmware updates and applying them where appropriate\nand approved by Client.\n2.3 Corrective Maintenance\nIn the event of a fault or malfunction of the Equipment, Service Provider shall:\na. Provide remote diagnostic support during Service Hours;\nb. Attend the Premises, where necessary, to repair or replace faulty parts;\nc. Restore the system to proper operating condition as soon as reasonably practicable,\nsubject to parts availability and site access.\n2.4 Exclusions\nThe Services do not include:\n• Repair of damage caused by vandalism, theft, fire, flood, lightning, power surges,\nor other force majeure events\n• Repair of damage caused by misuse, negligence, or unauthorised modification\nby Client or any third party\n• Relocation, redesign, or expansion of the system (e.g., adding new cameras or\ncabling routes)\n• Provision of monitoring centre services or internet connectivity\n• \nnt of NVR hard drives due to capacity upgrades requested by Client\n(as opposed to genuine failure).\nAny such excluded work may be carried out under a separate quotation and agreement.\n3. SERVICE LEVELS & RESPONSE TIMES\n3.1 Service Hours\nStandard service hours are Monday to Friday, 09:00 to 17:30 (UK time), excluding\nbank/public holidays in England and Wales (“Service Hours”).\n3.2 Reporting Faults\nClient shall report faults via email to support@guardiancameras.co.uk or by\ntelephone on 0161 123 4567, quoting the contract reference GC/Greenfield/2025.\n3.3 Response Times\n• Remote response time: within 4 business hours from receipt of the fault report\nduring Service Hours.\n• On-site response time: within 2 business days from receipt of the fault report\nduring Service Hours where an on-site visit is required.\n3.4 Resolution\nService Provider shall use reasonable endeavours to resolve faults as quickly as\npossible. Resolution times may vary depending on the complexity of the fault, parts\navailability, and site access arrangements.\n4. CLIENT OBLIGATIONS\nClient agrees to:\na. Provide Service Provider with reasonable access to the Premises and Equipment\nduring Service Hours;\nb. Ensure a representative is available to escort Service Provider’s personnel and sign\nservice reports;\nc. Maintain a safe working environment in compliance with health and safety legislation;\nd. Promptly notify Service Provider of any fault, suspected fault, or damage to the\nEquipment;\ne. Not permit any third party (other than Service Provider) to service, modify, or tamper\nwith the Equipment without Service Provider’s prior written consent, except in genuine\nemergencies.\n5. FEES & PAYMENT TERMS\n5.1 Maintenance Fees\nIn consideration of the Services, Client shall pay Service Provider:\n• A fixed annual maintenance fee of £4,800.00 (four thousand eight hundred\npounds) excluding VAT; and\n• The cost of \nnt parts not covered by the fixed fee, as set out in\nSchedule 2 (Parts Pricing).\n5.2 Payment Schedule\nThe annual maintenance fee shall be invoiced quarterly in advance in four equal\ninstalments of £1,200.00 excluding VAT, payable on or around:\n• 1 December 2025\n• 1 March 2026\n• 1 June 2026\n• 1 September 2026\n5.3 Payment Terms\nClient shall pay all undisputed invoices within 30 days of the invoice date by bank\ntransfer to the account details stated on the invoice.\n5.4 Late Payment\nIf Client fails to pay any undisputed amount by the due date, Service Provider may\ncharge interest at 4% per annum above the Bank of England base rate, accruing daily\nfrom the due date until payment is received in full.\n6. SPARE PARTS & \nNTS\n6.1 Parts\nService Provider shall use new or refurbished parts of equal or higher specification than\nthe original parts being replaced.\n6.2 Ownership\nAny parts removed from the Equipment become the property of Service Provider.\n\nnt parts installed become part of the Equipment owned by Client, once paid\nfor in full.\n7. REPORTING & DOCUMENTATION\n7.1 Service Reports\nAfter each preventive maintenance visit or corrective maintenance call-out, Service\nProvider shall provide a short written report, which will include:\n• Date and time of attendance\n• Work carried out\n• Equipment inspected or repaired\n• Any faults found and rectified\n• Any outstanding issues or recommendations.\n7.2 Records\nService Provider shall maintain records of maintenance visits, repairs, and parts\nreplaced for the duration of this Agreement and for at least 12 months after the End\nDate.\n8. DATA PROTECTION & PRIVACY\n8.1 Data Controller\nClient is and remains the data controller for all video and related data processed by the\nEquipment.\n8.2 Compliance\nClient is responsible for ensuring that the use of CCTV at the Premises complies with all\napplicable data protection and privacy laws in the United Kingdom, including the UK\nGDPR and Data Protection Act 2018 (for example, signage, privacy notices, retention\npolicies).\n8.3 Service Provider Access to Data\nWhere Service Provider needs access to live or recorded video data to perform the\nServices:\n• Access shall be limited to the minimum necessary;\n• Service Provider shall keep all such data confidential and shall not copy, retain,\nor disclose such data except as necessary to perform the Services or as required\nby law.\nIf required, the Parties may enter into a separate data processing agreement.\n9. CONFIDENTIALITY\nEach Party shall keep confidential all information of a technical, commercial, or\nsensitive nature received from the other Party in connection with this Agreement and\nshall not disclose it to any third party except:\n• To its employees, agents, or subcontractors who need to know such information\nfor the purposes of this Agreement and are bound by confidentiality obligations;\nor\n• As required by law, regulation, or court order.\nThis clause shall survive termination or expiry of this Agreement.\n10. LIABILITY & INSURANCE\n10.1 Limitation of Liability\nNothing in this Agreement limits or excludes either Party’s liability for:\n• Death or personal injury caused by its negligence;\n• Fraud or fraudulent misrepresentation; or\n• Any other liability that cannot be limited or excluded by law.\nSubject to the above:\na. Neither Party shall be liable to the other for any indirect or consequential loss,\nincluding loss of profit, loss of revenue, or loss of business; and\nb. Service Provider’s total aggregate liability arising out of or in connection with this\nAgreement shall not exceed the total maintenance fees actually paid by Client to\nService Provider under this Agreement in the 12 months preceding the event giving rise\nto the claim.\n10.2 Insurance\nService Provider shall maintain public liability insurance and professional indemnity\ninsurance at levels reasonably appropriate to the Services and shall provide evidence of\nsuch insurance upon reasonable request.\n11. TERMINATION\n11.1 Termination for Convenience\nEither Party may terminate this Agreement for convenience by giving 90 days’ written\nnotice to the other Party. Such notice may not expire before 31 May 2026, unless\notherwise agreed in writing by both Parties.\n11.2 Termination for Cause\nEither Party may terminate this Agreement immediately by written notice if the other\nParty:\na. Commits a material breach of this Agreement and, if the breach is capable of remedy,\nfails to remedy it within 30 days of receiving written notice specifying the breach; or\nb. Becomes insolvent, enters into administration, receivership, or liquidation, or ceases\nto carry on business.\n11.3 Effect of Termination\nUpon termination or expiry:\n• Service Provider shall cease providing the Services;\n• Client shall pay all outstanding fees for Services provided up to the effective date\nof termination;\n• Any pre-paid fees relating to Services not yet provided may be refunded on a prorata basis, if termination is due to Service Provider’s material breach and no\nremedy is offered.\n12. FORCE MAJEURE\nNeither Party shall be liable for any failure or delay in performing its obligations (other\nthan payment obligations) under this Agreement if such failure or delay is caused by\nevents beyond its reasonable control, including natural disasters, war, terrorism, civil\nunrest, strikes, failure of utilities, or government restrictions. The affected Party shall\nnotify the other Party as soon as reasonably practicable.\n13. GENERAL\n13.1 Governing Law and Jurisdiction\nThis Agreement shall be governed by and construed in accordance with the laws of\nEngland and Wales. The Parties submit to the exclusive jurisdiction of the courts of\nEngland and Wales.\n13.2 Entire Agreement\nThis Agreement, together with any Schedules attached, constitutes the entire\nagreement between the Parties in relation to its subject matter and supersedes all prior\nagreements, understandings, or representations, whether written or oral.\n13.3 Amendments\nNo amendment to this Agreement shall be effective unless it is in writing and signed by\nauthorised representatives of both Parties.\n13.4 Assignment\nNeither Party may assign or transfer its rights or obligations under this Agreement\nwithout the prior written consent of the other Party, except that either Party may assign\nthis Agreement to a successor entity in connection with a merger or sale of substantially\nall of its assets.\n13.5 Notices\nNotices under this Agreement shall be in writing and delivered by hand, by recorded\ndelivery post, or by email to:\n• For Client:\nGreenfield Office Park Ltd\n12 Greenfield Way, Birmingham, B1 2AB\nEmail: facilities@greenfieldoffice.co.uk\n• For Service Provider:\nGuardian Cameras & Security Ltd\n48 High Street, Manchester, M1 3CD\nEmail: contracts@guardiancameras.co.uk\nNotices shall be deemed received (a) if delivered by hand, on the date of delivery; (b) if\nsent by recorded delivery, two business days after posting; and (c) if sent by email, at\nthe time of transmission (provided no bounce-back is received).\n14. SIGNATURES\nIN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective\nDate.\nFor and on behalf of Greenfield Office Park Ltd (Client):\nName: _______________________________\nTitle: ________________________________\nSignature: ____________________________\nDate: ________________________________\nFor and on behalf of Guardian Cameras & Security Ltd (Service Provider):\nName: _______________________________\nTitle: ________________________________\nSignature: ____________________________\nDate: ________________________________ \n\n",
                "model": DOMAIN_MODEL,
                "options": {}
            }

            json_response = None
            try:
                response = requests.post(MCPS_API_URL, json=ai_payload, timeout = 120)
                response.raise_for_status()
                json_response = response.json()
            except Exception as e:
                print(e)
        
            # Handle case where request failed
            if json_response is None or 'result' not in json_response:
                structured_data = []
            else:
                structured_data = [parse_structured_msg([json_response['result']['response']])]

            payload = Message(
                role="bot",
                Msg="Response from DomainDrone",
                Images=[],
                structuredMsg=structured_data,
                Files=[],
                Videos=[]
            )
            return payload
    
        # upload document, process and transform to knowledge graph data
        @self.app.post("/documents")
        async def post_documents(file: UploadFile = File(...)):
            """
            Uploads a PDF file, extracts text using `process_document()`, stores chunked text with vectors in Neo4j.
            Ensures each chunk has a globally unique ID and is linked correctly only within its document.
            """
            if not file:
                raise HTTPException(status_code=400, detail="File is required")

            # Validate file type
            allowed_extensions = ["pdf", "docx", "txt", "xlsx"]
            file_extension = file.filename.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise HTTPException(status_code=415, detail="Unsupported file type")

            # Read file content
            file_content = await file.read()
            if not file_content:
                raise HTTPException(status_code=400, detail="File is empty or unreadable")

            try:
                # Generate a unique document ID
                document_id = file.filename.split(".")[0]  # Use filename as document ID

                # Call `process_document()` to extract text from PDF
                processed_data = process_document(file_content, file_extension,in_file_name=file.filename)
                if not processed_data:
                    raise HTTPException(
                        status_code=500, detail="Error processing PDF: no content extracted"
                    )

                # Chunk the extracted text
                chunks = chunk_text(processed_data)

                # Generate vector embeddings
                chunk_embeddings = embed_text(chunks)

                # Store in Neo4j
                with GraphDatabase.driver(
                    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
                ) as driver:
                    with driver.session() as session:
                        for i, chunk in enumerate(chunks):
                            unique_chunk_id = f"{document_id}_{i}"
                            
                            cleanliness = cleanliness_score(chunk)
                            
                            session.run(
                                """
                                CREATE (c:Chunk {
                                    chunk_id: $chunk_id,
                                    document_id: $document_id,
                                    text: $text,
                                    vector: $vector,
                                    cleanliness: $cleanliness
                                })
                                """,
                                chunk_id=unique_chunk_id,
                                document_id=document_id,
                                text=chunk,
                                vector=chunk_embeddings[i],
                                cleanliness=cleanliness,
                            )

                            if i > 0:
                                prev_chunk_id = f"{document_id}_{i - 1}"
                                session.run(
                                    """
                                    MATCH (c1:Chunk {chunk_id: $chunk1, document_id: $document_id}),
                                        (c2:Chunk {chunk_id: $chunk2, document_id: $document_id})
                                    CREATE (c1)-[:NEXT]->(c2)
                                    """,
                                    chunk1=prev_chunk_id,
                                    chunk2=unique_chunk_id,
                                    document_id=document_id,
                                )

                return {
                    "message": f"Document '{file.filename}' processed and stored in Neo4j.",
                    "document_id": document_id,
                    "total_chunks": len(chunks),
                }

            except Exception as e:
                logging.error(f"Error processing PDF: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Internal error during processing: {e}"
                )


        @self.app.get("/batch")
        async def process_batch():
            """
            Processes all files in the 'batch' folder by sending them one at a time to the '/documents' endpoint.
            Deletes each file after successful processing and streams real-time progress updates.
            """
            batch_folder = "batch"

            # Ensure the batch folder exists
            if not os.path.exists(batch_folder):
                raise HTTPException(status_code=400, detail="Batch folder does not exist.")

            files = [
                f
                for f in os.listdir(batch_folder)
                if os.path.isfile(os.path.join(batch_folder, f))
            ]

            if not files:
                raise HTTPException(
                    status_code=400, detail="No files to process in the batch folder."
                )

            total_files = len(files)

            async def process_files():
                for idx, filename in enumerate(files, start=1):
                    file_path = os.path.join(batch_folder, filename)

                    try:
                        with open(file_path, "rb") as file:
                            file_content = file.read()
                            file_like = io.BytesIO(
                                file_content
                            )  # Convert bytes into a file-like object

                            file_upload = UploadFile(filename=filename, file=file_like)

                            # Send file to /documents endpoint
                            response = await post_documents(file_upload)

                            # Delete the file after successful processing
                            os.remove(file_path)

                            yield f'data: {{"file": "{filename}", "status": "processed", "progress": "{idx} of {total_files}"}}\n\n'

                        # Simulate a small delay (optional, for better streaming effect)
                        await asyncio.sleep(0.5)

                    except Exception as e:
                        logging.error(f"Error processing file {filename}: {e}")
                        yield f'data: {{"file": "{filename}", "status": "failed: {str(e)}", "progress": "{idx} of {total_files}"}}\n\n'

                yield f'data: {{"message": "Batch processing completed."}}\n\n'

            return StreamingResponse(process_files(), media_type="text/event-stream")

        def cleanliness_score(text: str):
            valid = sum(c.isalnum() or c.isspace() or c in ".,;:-()" for c in text)
            return valid / max(len(text), 1)