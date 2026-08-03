from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes.auth import router as auth_router
from routes.classes import router as classes_router
from routes.readings import router as readings_router
from routes.notes import router as notes_router
from routes.todos import router as todos_router
from models import Base, User
from database import engine, SessionLocal
from auth import get_password_hash

load_dotenv()

Base.metadata.create_all(bind=engine)

def create_default_user():
    db = SessionLocal()
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        hashed_password = get_password_hash("admin123")
        admin_user = User(username="admin", password_hash=hashed_password)
        db.add(admin_user)
        db.commit()
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

@app.on_event("startup")
def startup_event():
    create_default_user()

@app.get("/")
def read_root():
    return {"message": "3L Academic Hub API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
