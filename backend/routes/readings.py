from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Reading, Class, User
from schemas import ReadingCreate, ReadingResponse
from auth import get_current_user

router = APIRouter(prefix="/readings", tags=["readings"])

@router.post("/", response_model=ReadingResponse)
def create_reading(reading_data: ReadingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_class = db.query(Class).filter(
        Class.id == reading_data.class_id,
        Class.user_id == current_user.id
    ).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")

    db_reading = Reading(
        class_id=reading_data.class_id,
        title=reading_data.title,
        source=reading_data.source,
        assigned_date=reading_data.assigned_date,
        due_date=reading_data.due_date,
        status=reading_data.status,
        pages_total=reading_data.pages_total
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.get("/", response_model=list[ReadingResponse])
def get_readings(class_id: int = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Reading).join(Class).filter(Class.user_id == current_user.id)
    if class_id:
        query = query.filter(Reading.class_id == class_id)
    return query.all()

@router.get("/{reading_id}", response_model=ReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return db_reading

@router.put("/{reading_id}", response_model=ReadingResponse)
def update_reading(reading_id: int, reading_data: ReadingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    db_reading.title = reading_data.title
    db_reading.source = reading_data.source
    db_reading.assigned_date = reading_data.assigned_date
    db_reading.due_date = reading_data.due_date
    db_reading.status = reading_data.status
    db_reading.pages_total = reading_data.pages_total
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.patch("/{reading_id}", response_model=ReadingResponse)
def update_reading_progress(reading_id: int, pages_read: int = None, reading_time_minutes: int = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    if pages_read is not None:
        db_reading.pages_read = pages_read
    if reading_time_minutes is not None:
        db_reading.reading_time_minutes = reading_time_minutes
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.delete("/{reading_id}")
def delete_reading(reading_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    db.delete(db_reading)
    db.commit()
    return {"message": "Reading deleted"}
