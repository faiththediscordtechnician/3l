import sys
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="3L Academic Hub", version="1.0.0")
print("✓ FastAPI app created")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://3l-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    print("Loading auth router...")
    from routes.auth import router as auth_router
    app.include_router(auth_router)
    print("✓ Auth router loaded")
except Exception as e:
    print(f"✗ Warning: Could not load auth router: {e}")
    import traceback
    traceback.print_exc()

try:
    from routes.classes import router as classes_router
    app.include_router(classes_router)
except Exception as e:
    print(f"Warning: Could not load classes router: {e}")

try:
    from routes.readings import router as readings_router
    app.include_router(readings_router)
except Exception as e:
    print(f"Warning: Could not load readings router: {e}")

try:
    from routes.notes import router as notes_router
    app.include_router(notes_router)
except Exception as e:
    print(f"Warning: Could not load notes router: {e}")

try:
    from routes.todos import router as todos_router
    app.include_router(todos_router)
except Exception as e:
    print(f"Warning: Could not load todos router: {e}")

try:
    from routes.search import router as search_router
    app.include_router(search_router)
except Exception as e:
    print(f"Warning: Could not load search router: {e}")

try:
    from routes.annotations import router as annotations_router
    app.include_router(annotations_router)
except Exception as e:
    print(f"Warning: Could not load annotations router: {e}")

try:
    from routes.export import router as export_router
    app.include_router(export_router)
except Exception as e:
    print(f"Warning: Could not load export router: {e}")

try:
    from routes.sync import router as sync_router
    app.include_router(sync_router)
except Exception as e:
    print(f"Warning: Could not load sync router: {e}")

try:
    from routes.setup import router as setup_router
    app.include_router(setup_router)
except Exception as e:
    print(f"Warning: Could not load setup router: {e}")

@app.on_event("startup")
async def startup_event():
    print("🚀 3L Academic Hub starting...")

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}
