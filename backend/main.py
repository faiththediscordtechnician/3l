from fastapi import FastAPI

app = FastAPI(title="3L Academic Hub", version="1.0.0")

# Test with just auth router
try:
    from routes.auth import router as auth_router
    app.include_router(auth_router)
except Exception as e:
    print(f"Warning: Auth router failed: {e}")

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}
