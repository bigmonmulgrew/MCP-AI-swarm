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
            "stream": False, 
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

# ==========================================================
# Local Debug Test (when running python main.py directly)
# ==========================================================
if __name__ == "__main__":
    import asyncio
    
    from config import OLLAMA_DEBUG_URL

    # Override environment value for local testing
    
    OLLAMA_URL = OLLAMA_DEBUG_URL
    print(f"[AIQ] Using DEBUG OLLAMA URL: {OLLAMA_URL}")

    async def debug_test():
        
        
        print("\n[AIQ] Running local debug test...\n")

        # Start the worker manually (FastAPI normally does this)
        asyncio.create_task(ai_worker())

        # Give the worker a moment to start
        await asyncio.sleep(0.2)

        # Create two jobs
        job1 = AIQuery(
            prompt="Hello, how are you today?",
            model="phi4"
        )
        job2 = AIQuery(
            prompt="Give me a small maths sum for a primary school child.",
            model="phi4"
        )

        # Get event loop
        loop = asyncio.get_event_loop()

        # Create futures manually
        future1 = loop.create_future()
        future2 = loop.create_future()

        # Create job IDs
        job_id1 = str(uuid.uuid4())
        job_id2 = str(uuid.uuid4())

        # Enqueue jobs exactly like API would
        await queue.put((job_id1, job1, future1))
        print(f"[TEST] Queued job {job_id1}")

        await queue.put((job_id2, job2, future2))
        print(f"[TEST] Queued job {job_id2}")

        # Await their completion
        result1 = await future1
        result2 = await future2

        print("\n==================== RESULTS ====================")
        print(f"Job {job_id1}: {result1}\n")
        print(f"Job {job_id2}: {result2}\n")
        print("================================================\n")

    asyncio.run(debug_test())
