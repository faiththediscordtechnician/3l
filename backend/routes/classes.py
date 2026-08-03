from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Class, User
from schemas import ClassCreate, ClassResponse
from auth import get_current_user

router = APIRouter(prefix="/classes", tags=["classes"])

@router.post("/", response_model=ClassResponse)
def create_class(class_data: ClassCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_class = Class(
        user_id=current_user.id,
        name=class_data.name,
        code=class_data.code,
        instructor=class_data.instructor,
        notes=class_data.notes,
        color=class_data.color
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@router.get("/", response_model=list[ClassResponse])
def get_classes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Class).filter(Class.user_id == current_user.id).all()

@router.get("/{class_id}", response_model=ClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_class = db.query(Class).filter(
        Class.id == class_id,
        Class.user_id == current_user.id
    ).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@router.put("/{class_id}", response_model=ClassResponse)
def update_class(class_id: int, class_data: ClassCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_class = db.query(Class).filter(
        Class.id == class_id,
        Class.user_id == current_user.id
    ).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")

    db_class.name = class_data.name
    db_class.code = class_data.code
    db_class.instructor = class_data.instructor
    db_class.notes = class_data.notes
    db_class.color = class_data.color
    db.commit()
    db.refresh(db_class)
    return db_class

@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_class = db.query(Class).filter(
        Class.id == class_id,
        Class.user_id == current_user.id
    ).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")

    db.delete(db_class)
    db.commit()
    return {"message": "Class deleted"}
