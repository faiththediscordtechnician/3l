#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal
from backend.models import User
from backend.auth import get_password_hash

def add_user(username: str, password: str):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"User '{username}' already exists")
            return False

        hashed_password = get_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✓ User '{username}' created successfully (ID: {new_user.id})")
        return True
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    add_user("marie", "jdorbust")
