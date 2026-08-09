import sys
print("Starting application initialization...", file=sys.stderr)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

print("Loading environment variables...", file=sys.stderr)
try:
    load_dotenv()
    print("Environment variables loaded", file=sys.stderr)
except Exception as e:
    print(f"Error loading environment variables: {e}", file=sys.stderr)

print("Creating FastAPI app...", file=sys.stderr)
app = FastAPI(title="3L Academic Hub", version="1.0.0")
print("FastAPI app created", file=sys.stderr)

# Import and register routers
try:
    from routes.auth import router as auth_router
    app.include_router(auth_router)
except Exception as e:
    print(f"Warning: Auth router failed: {e}")

try:
    from routes.classes import router as classes_router
    app.include_router(classes_router)
except Exception as e:
    print(f"Warning: Classes router failed: {e}")

try:
    from routes.readings import router as readings_router
    app.include_router(readings_router)
except Exception as e:
    print(f"Warning: Readings router failed: {e}")

try:
    from routes.notes import router as notes_router
    app.include_router(notes_router)
except Exception as e:
    print(f"Warning: Notes router failed: {e}")

try:
    from routes.todos import router as todos_router
    app.include_router(todos_router)
except Exception as e:
    print(f"Warning: Todos router failed: {e}")

try:
    from routes.search import router as search_router
    app.include_router(search_router)
except Exception as e:
    print(f"Warning: Search router failed: {e}")

try:
    from routes.annotations import router as annotations_router
    app.include_router(annotations_router)
except Exception as e:
    print(f"Warning: Annotations router failed: {e}")

try:
    from routes.export import router as export_router
    app.include_router(export_router)
except Exception as e:
    print(f"Warning: Export router failed: {e}")

try:
    from routes.sync import router as sync_router
    app.include_router(sync_router)
except Exception as e:
    print(f"Warning: Sync router failed: {e}")

try:
    from routes.setup import router as setup_router
    app.include_router(setup_router)
except Exception as e:
    print(f"Warning: Setup router failed: {e}")

print("All routers loaded", file=sys.stderr)

print("Adding CORS middleware...", file=sys.stderr)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Middleware added", file=sys.stderr)

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"pong": True}

print("Application initialized successfully!", file=sys.stderr)
