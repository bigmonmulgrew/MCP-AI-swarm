import asyncio
import uuid
import requests
from fastapi import FastAPI
from common import AIQuery
from config import *

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(title="AI Queue System Running")

# --------------------------------------------------
# Internal Queue
# --------------------------------------------------
queue = asyncio.Queue()
semaphore = asyncio.Semaphore(MAX_CONCURRENT)

# --------------------------------------------------
# Worker: runs forever, processing queued jobs
# --------------------------------------------------
async def ai_worker():
    print("[AIQ] Worker started...")
    while True:
        job_id, ai_query, future = await queue.get()

        print(f"[AIQ] Processing job {job_id} -> model={ai_query.model}")

        try:
            # Only one worker allowed at a time
            async with semaphore:
                result = await call_ollama(ai_query)
                future.set_result({"job_id": job_id, "result": result})
        except Exception as e:
            future.set_result({"job_id": job_id, "error": str(e)})

        queue.task_done()


# --------------------------------------------------
# Ollama Call (wrapped as async)
# --------------------------------------------------
async def call_ollama(query: AIQuery):
    """
    Standard Ollama API call.
    This wraps the sync requests.post in an async executor.
    """
    def _sync_call():
        payload = {
            "model": query.model,
            "prompt": query.prompt,
            "options": query.options
        }
        res = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=False)
        res.raise_for_status()
        return res.json()

    # Run sync call in thread so FastAPI stays async-safe
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _sync_call)


# --------------------------------------------------
# Startup: launch worker(s)
# --------------------------------------------------
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(ai_worker())
    print("[AIQ] Startup complete, worker running.")


# --------------------------------------------------
# API Endpoints
# --------------------------------------------------
@app.get("/status")
def status():
    return {"status": "ok", "queue_size": queue.qsize()}


@app.post("/query")
async def enqueue_ai_job(data: AIQuery):
    """
    Adds an AI job to the queue and waits for its completion.
    """
    job_id = str(uuid.uuid4())
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    await queue.put((job_id, data, future))

    print(f"[AIQ] Job {job_id} queued. Current queue size: {queue.qsize()}")

    # Wait for worker to resolve the future
    result = await future
    return result
