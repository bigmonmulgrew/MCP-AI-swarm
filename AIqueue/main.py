from fastapi import FastAPI

app = FastAPI(title="AI queue system running")

@app.get("/status")
def status():
    return {"status": "ok"}

@app.get("/query")
def status():
    return {"status": "not imnplemented"}