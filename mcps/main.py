from fastapi import FastAPI

app = FastAPI(title="Multi Cotext Protocole Server API is runnning")

@app.get("/")
def read_root():
    return {"message": "Multi Cotext Protocole Server API is running"}

@app.get("/status")
def status():
    return {"status": "ok"}