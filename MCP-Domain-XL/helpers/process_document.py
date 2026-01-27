import logging
from markitdown import MarkItDown
import docx  # python-docx for DOCX handling
from io import BytesIO
from uuid import uuid4
import os
import shutil
import ocrmypdf
import tempfile
import utils

OPTIMISE_IMAGE_PDFS = utils.env_bool("OPTIMISE_IMAGE_PDFS", default=False)  
PDF_OUTPUT_FOLDER = os.getenv("PDF_OUTPUT_FOLDER", "./optimised")      # relative to API folder. Default is ./optimised

def process_document(file, file_extension, in_file_name = ""):
    """
    Processes a document based on its file extension.

    Args:
        file (bytes): The binary content of the document.
        file_extension (str): The file extension (e.g., "pdf", "docx", "txt").

    Returns:
        dict: A dictionary containing the extracted content or None if an error occurs.
    """
    logging.debug(f"Processing document of type: {file_extension}")
    temp_dir = None
    
    try:
        unique_id = uuid4()            
        temp_dir = f"../temp/{unique_id}"
        os.makedirs(temp_dir, exist_ok=True)

        filename = f"{uuid4()}.{file_extension}"
        file_path = os.path.join(temp_dir, filename)

        with open(file_path, "wb") as f:
            f.write(file)
        
        md = MarkItDown()        
        result = md.convert(file_path)
        
        text = result.text_content or ""
        
        if file_extension == "pdf" and len(text.strip()) < 10:
            logging.warning("PDF appears to contain no text layer (image-only PDF)")
            text = extract_from_image(file_path,in_file_name) or ""
        
        
        logging.info(text)
        return text

    except Exception as e:
        logging.error(f"Error processing document: {e}")
        return None
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def extract_from_image(pdf_path: str, in_file_name: str = "") -> str:
    logging.info(f"Running OCR conversion: {pdf_path}")
    ocr_output = pdf_path.replace(".pdf", "_ocr.pdf")

    if (in_file_name == ""):
        in_file_name = pdf_path
        
    # 1. Generate unoptimised OCR PDF (authoritative for text)
    ocrmypdf.ocr(
        pdf_path,
        ocr_output,
        skip_text=True,
        deskew=True,
        rotate_pages=True,
        optimize=0,
        oversample=300,
        progress_bar=False
    )

    # 2. Optionally generate optimised copy for storage
    if OPTIMISE_IMAGE_PDFS:
        logging.info(f"Generating OCR enabled copy: {in_file_name}")
        try:
            os.makedirs(PDF_OUTPUT_FOLDER, exist_ok=True)
            
            safe_name = os.path.basename(in_file_name)
            safe_name = os.path.splitext(safe_name)[0] + ".pdf"

            optimised_path = os.path.join(
                PDF_OUTPUT_FOLDER,
                safe_name
            )

            ocrmypdf.ocr(
                pdf_path,
                optimised_path,
                skip_text=True,
                deskew=True,
                rotate_pages=True,
                optimize=1,
                oversample=300,
                progress_bar=False
            )
            logging.info(f"OCR complete and saved to: {optimised_path}")
        except Exception as e:
            logging.warning(f"OCR optimisation skipped: {e}")

    # 3. Extract text
    md = MarkItDown()
    result = md.convert(ocr_output)

    text = (result.text_content or "").strip()
    if len(text) < 10:
        raise RuntimeError("OCR completed but no text extracted")

    return text
