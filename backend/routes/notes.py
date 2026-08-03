from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Note, Reading, Class, User
from schemas import NoteCreate, NoteResponse
from auth import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == note_data.reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    db_note = Note(
        reading_id=note_data.reading_id,
        title=note_data.title,
        content=note_data.content,
        tags=note_data.tags or {}
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=list[NoteResponse])
def get_notes(reading_id: int = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Note).join(Reading).join(Class).filter(Class.user_id == current_user.id)
    if reading_id:
        query = query.filter(Note.reading_id == reading_id)
    return query.all()

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Note).join(Reading).join(Class).filter(
        Note.id == note_id,
        Class.user_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Note).join(Reading).join(Class).filter(
        Note.id == note_id,
        Class.user_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db_note.title = note_data.title
    db_note.content = note_data.content
    db_note.tags = note_data.tags or {}
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Note).join(Reading).join(Class).filter(
        Note.id == note_id,
        Class.user_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted"}
