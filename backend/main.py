from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
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
from models import Base, User
from database import engine, SessionLocal, verify_database_connection
from auth import get_password_hash

load_dotenv()

Base.metadata.create_all(bind=engine)

def create_default_user():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            hashed_password = get_password_hash("admin123")
            admin_user = User(username="admin", password_hash=hashed_password)
            db.add(admin_user)
            db.commit()
            print("✓ Default admin user created")
    except Exception as e:
        print(f"✗ Error creating default user: {e}")
        db.rollback()
    finally:
        db.close()

app = FastAPI(title="3L Academic Hub", version="1.0.0")

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
def startup_event():
    create_default_user()

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
