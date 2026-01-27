# embeds text passed to it and returns as a list of vector id's
from dotenv import load_dotenv
import os
import logging
import time

from langchain_ollama import OllamaEmbeddings
from openai import OpenAI

# Configure logging to show debug messages
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
# check env for embeddings location, local or remote API
embed_location = os.getenv("EMBED_LOCATION_ENV", "ollama")

# load the OpenAI API key
OpenAI.api_key = os.getenv("OPENAI_API_KEY", None)

# add ollama driver here
LLM_EMBEDDING_DEFAULT_MODEL = os.getenv(
    "LLM_EMBEDDING_MODEL", "tazarov/all-minilm-l6-v2-f32"
)
llm_base_url = "http://ollama-container:11434/"
ollama_embed = OllamaEmbeddings(
    base_url=llm_base_url, model=LLM_EMBEDDING_DEFAULT_MODEL
)

# add OpenAI driver here
client = OpenAI()
open_ai_model = "text-embedding-3-small"


def embed_text(query: list[str]):
    """
    Takes the passed text and creates sentenceTransformer emdeddings and returns them as a list.
    """
    # Debug: Log the received query.
    logging.debug("Received query: %s", query)

    query_embedding = []

    # check for location of LLMS from embed_location
    if embed_location == "ollama":

        for q in query:
            # Compute the embedding for the query text.
            try:
                query_embedding.append(ollama_embed.embed_query(q))
            except Exception as e:
                logging.error(e)

    else:
        for q in query:
            # Compute the embedding for the query text.
            try:
                response = client.embeddings.create(model=open_ai_model, input=q)
                query_embedding.append(response.data[0].embedding)
                time.sleep(1)
                logging.info("Sleeping...")
            except Exception as e:
                logging.error(e)

    # Debug: Log the embedding values.
    logging.debug("Computed query embedding: %s", query_embedding)

    return query_embedding
