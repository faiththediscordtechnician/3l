from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Note
from schemas import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=list[NoteResponse])
async def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).order_by(Note.pinned.desc(), Note.updated_at.desc()).all()
    return notes

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = note.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"status": "deleted"}
