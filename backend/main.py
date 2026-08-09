from fastapi import FastAPI
import sys

app = FastAPI(title="3L Academic Hub", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    print("✓ App startup event triggered", file=sys.stderr, flush=True)

@app.on_event("shutdown")
async def shutdown_event():
    print("✗ App shutdown event triggered", file=sys.stderr, flush=True)

# Test with just auth router
try:
    from routes.auth import router as auth_router
    app.include_router(auth_router)
except Exception as e:
    print(f"Warning: Auth router failed: {e}", file=sys.stderr, flush=True)

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}
