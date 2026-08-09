from fastapi import FastAPI
import sys
import traceback

try:
    app = FastAPI(title="3L Academic Hub", version="1.0.0")
    print("✓ FastAPI app created", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to create FastAPI app: {e}", file=sys.stderr, flush=True)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

@app.on_event("startup")
async def startup_event():
    print("✓ App startup event triggered", file=sys.stderr, flush=True)

@app.on_event("shutdown")
async def shutdown_event():
    print("✗ App shutdown event triggered", file=sys.stderr, flush=True)

# Test with just auth router
try:
    print("Attempting to import auth router...", file=sys.stderr, flush=True)
    from routes.auth import router as auth_router
    app.include_router(auth_router)
    print("✓ Auth router added", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Auth router failed: {e}", file=sys.stderr, flush=True)
    traceback.print_exc(file=sys.stderr)

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}

print("✓ Main.py loaded successfully", file=sys.stderr, flush=True)
