from fastapi import FastAPI
import sys
import os

print("Loading main.py...", file=sys.stderr, flush=True)

app = FastAPI(title="3L Academic Hub", version="1.0.0")

print("FastAPI app created", file=sys.stderr, flush=True)

@app.on_event("startup")
async def startup():
    port = os.getenv("PORT", "8000")
    print(f"✓ APP READY - Listening on port {port}", file=sys.stderr, flush=True)

@app.get("/")
def read_root():
    print("GET / called", file=sys.stderr, flush=True)
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    print("GET /health called", file=sys.stderr, flush=True)
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    print("GET /ping called", file=sys.stderr, flush=True)
    return {"pong": True}

print("main.py loaded - app ready", file=sys.stderr, flush=True)
