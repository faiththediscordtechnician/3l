from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="3L Academic Hub", version="1.0.0")

# Import and register auth router (core functionality)
try:
    from routes.auth import router as auth_router
    app.include_router(auth_router)
except Exception as e:
    print(f"Warning: Auth router failed to load: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}
