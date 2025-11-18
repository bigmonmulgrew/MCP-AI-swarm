import os
# --------------------------------------------------
# Config
# --------------------------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")
MAX_CONCURRENT = os.getenv("AI_MAX_CONCURRENT", 1)  # For now, strictly one worker