from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        print(f"User '{user.username}' not found in database", file=sys.stderr, flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_valid = verify_password(user.password, db_user.password_hash)
    if not password_valid:
        print(f"Password verification failed for user '{user.username}'", file=sys.stderr, flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    print(f"Login successful for user '{user.username}'", file=sys.stderr, flush=True)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [{"id": u.id, "username": u.username} for u in users]}

@router.post("/debug/create-test-user")
def create_test_user_endpoint(db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.username == "marie").first()
        if existing_user:
            return {"status": "User already exists", "user_id": existing_user.id}

        hashed_password = get_password_hash("jdorbust")
        new_user = User(username="marie", password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✓ Test user created via endpoint: ID {new_user.id}", file=sys.stderr, flush=True)
        return {"status": "User created successfully", "user_id": new_user.id, "username": "marie"}
    except Exception as e:
        print(f"✗ Error creating user: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
