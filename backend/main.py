from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine, verify_database_connection

print("Importing routers...", file=sys.stderr, flush=True)
try:
    from routes.auth import router as auth_router
    print("✓ auth router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import auth router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.classes import router as classes_router
    print("✓ classes router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import classes router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.readings import router as readings_router
    print("✓ readings router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import readings router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.notes import router as notes_router
    print("✓ notes router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import notes router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.todos import router as todos_router
    print("✓ todos router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import todos router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.search import router as search_router
    print("✓ search router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import search router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.annotations import router as annotations_router
    print("✓ annotations router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import annotations router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.export import router as export_router
    print("✓ export router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import export router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.sync import router as sync_router
    print("✓ sync router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import sync router: {e}", file=sys.stderr, flush=True)
    raise

try:
    from routes.setup import router as setup_router
    print("✓ setup router imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"✗ Failed to import setup router: {e}", file=sys.stderr, flush=True)
    raise

print("All routers imported successfully", file=sys.stderr, flush=True)

load_dotenv()

print("Loading main.py...", file=sys.stderr, flush=True)

try:
    app = FastAPI(title="3L Academic Hub", version="1.0.0")
except Exception as e:
    print(f"ERROR creating FastAPI app: {e}", file=sys.stderr, flush=True)
    raise

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
