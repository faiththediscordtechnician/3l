from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="3L Academic Hub", version="1.0.0")

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
