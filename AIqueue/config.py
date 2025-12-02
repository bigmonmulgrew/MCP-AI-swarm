import os
# --------------------------------------------------
# Config
# --------------------------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_DEBUG_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")

raw = os.getenv("AI_MAX_CONCURRENT", "1").strip().replace('"', '').replace("'", "") # ENV variables are strings and this upsets the strong typing in some of the libraries.
MAX_CONCURRENT = max(1, int(raw))  # For now, strictly one worker