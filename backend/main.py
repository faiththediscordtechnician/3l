from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine, verify_database_connection
from routes.auth import router as auth_router
from routes.classes import router as classes_router
from routes.readings import router as readings_router
from routes.notes import router as notes_router
from routes.todos import router as todos_router
from routes.search import router as search_router
from routes.annotations import router as annotations_router
from routes.export import router as export_router
from routes.sync import router as sync_router
from routes.setup import router as setup_router

load_dotenv()

print("Loading main.py...", file=sys.stderr, flush=True)

app = FastAPI(title="3L Academic Hub", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("FastAPI app created", file=sys.stderr, flush=True)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(classes_router)
app.include_router(readings_router)
app.include_router(notes_router)
app.include_router(todos_router)
app.include_router(search_router)
app.include_router(annotations_router)
app.include_router(export_router)
app.include_router(sync_router)
app.include_router(setup_router)

@app.on_event("startup")
async def startup():
    port = os.getenv("PORT", "8000")
    print(f"✓ APP READY - Listening on port {port}", file=sys.stderr, flush=True)
    if not verify_database_connection():
        print("⚠ Database connection failed but app will continue", file=sys.stderr, flush=True)

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}

print("main.py loaded - all routers registered", file=sys.stderr, flush=True)
