from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import User, Class, Reading, Note, TodoItem, Annotation
from auth import get_current_user

router = APIRouter(prefix="/sync", tags=["sync"])

@router.get("/status")
async def sync_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sync status and data summary"""
    try:
        classes_count = db.query(Class).filter(Class.user_id == current_user.id).count()
        readings_count = db.query(Reading).join(Class).filter(Class.user_id == current_user.id).count()
        notes_count = db.query(Note).join(Reading).join(Class).filter(Class.user_id == current_user.id).count()
        todos_count = db.query(TodoItem).filter(TodoItem.user_id == current_user.id).count()
        annotations_count = db.query(Annotation).join(Reading).join(Class).filter(Class.user_id == current_user.id).count()

        return {
            "status": "synced",
            "timestamp": datetime.utcnow().isoformat(),
            "user": current_user.username,
            "data": {
                "classes": classes_count,
                "readings": readings_count,
                "notes": notes_count,
                "todos": todos_count,
                "annotations": annotations_count,
            },
            "total_items": classes_count + readings_count + notes_count + todos_count + annotations_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync status check failed: {str(e)}")

@router.get("/full-export")
async def full_export(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export all user data for backup"""
    try:
        data = {
            "user": current_user.username,
            "exported_at": datetime.utcnow().isoformat(),
            "classes": [],
            "todos": [],
        }

        classes = db.query(Class).filter(Class.user_id == current_user.id).all()
        for cls in classes:
            class_data = {
                "id": cls.id,
                "name": cls.name,
                "code": cls.code,
                "instructor": cls.instructor,
                "notes": cls.notes,
                "color": cls.color,
                "readings": [],
            }

            readings = db.query(Reading).filter(Reading.class_id == cls.id).all()
            for reading in readings:
                reading_data = {
                    "id": reading.id,
                    "title": reading.title,
                    "source": reading.source,
                    "status": reading.status,
                    "pages_total": reading.pages_total,
                    "pages_read": reading.pages_read,
                    "reading_time_minutes": reading.reading_time_minutes,
                    "due_date": reading.due_date.isoformat() if reading.due_date else None,
                    "notes": [],
                    "annotations": [],
                }

                notes = db.query(Note).filter(Note.reading_id == reading.id).all()
                for note in notes:
                    reading_data["notes"].append({
                        "id": note.id,
                        "title": note.title,
                        "content": note.content,
                        "tags": note.tags,
                        "created_at": note.created_at.isoformat(),
                    })

                annotations = db.query(Annotation).filter(Annotation.reading_id == reading.id).all()
                for annotation in annotations:
                    reading_data["annotations"].append({
                        "id": annotation.id,
                        "text": annotation.text,
                        "highlight_color": annotation.highlight_color,
                        "page_number": annotation.page_number,
                    })

                class_data["readings"].append(reading_data)

            data["classes"].append(class_data)

        todos = db.query(TodoItem).filter(TodoItem.user_id == current_user.id).all()
        for todo in todos:
            data["todos"].append({
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "priority": todo.priority,
                "due_date": todo.due_date.isoformat() if todo.due_date else None,
                "class_id": todo.class_id,
            })

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full export failed: {str(e)}")

@router.post("/force-sync")
async def force_sync(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Force sync - verify all data is in database"""
    try:
        db.commit()
        status = await sync_status(db=db, current_user=current_user)
        return {
            "message": "Sync completed successfully",
            "sync_status": status,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Force sync failed: {str(e)}")

@router.get("/last-sync")
async def last_sync(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get timestamp of last sync"""
    try:
        latest_update = None

        readings = db.query(Reading).join(Class).filter(
            Class.user_id == current_user.id
        ).order_by(Reading.updated_at.desc()).first()
        if readings:
            latest_update = readings.updated_at

        notes = db.query(Note).join(Reading).join(Class).filter(
            Class.user_id == current_user.id
        ).order_by(Note.updated_at.desc()).first()
        if notes and (not latest_update or notes.updated_at > latest_update):
            latest_update = notes.updated_at

        todos = db.query(TodoItem).filter(
            TodoItem.user_id == current_user.id
        ).order_by(TodoItem.updated_at.desc()).first()
        if todos and (not latest_update or todos.updated_at > latest_update):
            latest_update = todos.updated_at

        return {
            "last_sync": latest_update.isoformat() if latest_update else None,
            "sync_time": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get last sync failed: {str(e)}")
