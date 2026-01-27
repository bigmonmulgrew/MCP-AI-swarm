import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define .env variables
CHUNK_SIZE_ENV = os.getenv("CHUNK_SIZE_ENV", 1500)
CHUNK_OVERLAP_ENV = os.getenv("CHUNK_OVERLAP_ENV", 200)

# Chunking settings
CHUNK_SIZE = int(CHUNK_SIZE_ENV)
CHUNK_OVERLAP = int(CHUNK_OVERLAP_ENV)

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """
    Splits text into chunks of specified size with overlap.

    :param text: The full text to be chunked.
    :param chunk_size: The maximum size of each chunk.
    :param chunk_overlap: The number of overlapping characters between chunks.
    :return: A list of chunked text segments.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)
