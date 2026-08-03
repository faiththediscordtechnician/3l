from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Annotation, Reading, Class, User
from schemas import AnnotationCreate, AnnotationResponse
from auth import get_current_user

router = APIRouter(prefix="/annotations", tags=["annotations"])

@router.post("/", response_model=AnnotationResponse)
def create_annotation(annotation_data: AnnotationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == annotation_data.reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    db_annotation = Annotation(
        reading_id=annotation_data.reading_id,
        text=annotation_data.text,
        highlight_color=annotation_data.highlight_color,
        page_number=annotation_data.page_number
    )
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

@router.get("/", response_model=list[AnnotationResponse])
def get_annotations(reading_id: int = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Annotation).join(Reading).join(Class).filter(Class.user_id == current_user.id)
    if reading_id:
        query = query.filter(Annotation.reading_id == reading_id)
    return query.all()

@router.get("/{annotation_id}", response_model=AnnotationResponse)
def get_annotation(annotation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_annotation = db.query(Annotation).join(Reading).join(Class).filter(
        Annotation.id == annotation_id,
        Class.user_id == current_user.id
    ).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return db_annotation

@router.put("/{annotation_id}", response_model=AnnotationResponse)
def update_annotation(annotation_id: int, annotation_data: AnnotationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_annotation = db.query(Annotation).join(Reading).join(Class).filter(
        Annotation.id == annotation_id,
        Class.user_id == current_user.id
    ).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")

    db_annotation.text = annotation_data.text
    db_annotation.highlight_color = annotation_data.highlight_color
    db_annotation.page_number = annotation_data.page_number
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

@router.delete("/{annotation_id}")
def delete_annotation(annotation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_annotation = db.query(Annotation).join(Reading).join(Class).filter(
        Annotation.id == annotation_id,
        Class.user_id == current_user.id
    ).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")

    db.delete(db_annotation)
    db.commit()
    return {"message": "Annotation deleted"}
