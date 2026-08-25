from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import User, Class
from auth import get_current_user

router = APIRouter(prefix="/setup", tags=["setup"])

DEFAULT_CLASSES = [
    {
        "name": "MEDIATION THEORY AND PRACTICE",
        "code": "CML 2320",
        "instructor": "Emilia Péch",
        "day_of_week": "Wednesday",
        "start_time": "17:30",
        "end_time": "20:20",
        "room": "120 University (FSS) 14001",
    },
    {
        "name": "LABOUR LAW I",
        "code": "CML 3233",
        "instructor": "Ravi A. Malhotra",
        "day_of_week": "Monday",
        "start_time": "14:30",
        "end_time": "15:50",
        "room": "57 Louis Pasteur (FTX) 137",
    },
    {
        "name": "LABOUR LAW I",
        "code": "CML 3233",
        "instructor": "Ravi A. Malhotra",
        "day_of_week": "Wednesday",
        "start_time": "13:00",
        "end_time": "14:20",
        "room": "57 Louis Pasteur (FTX) 137",
    },
    {
        "name": "STUDIES IN PUBLIC LAW",
        "code": "CML 4104",
        "instructor": "Andres Drew",
        "day_of_week": "Monday",
        "start_time": "16:00",
        "end_time": "18:50",
        "room": "57 Louis Pasteur (FTX) 413",
    },
    {
        "name": "STUDIES IN INTERNATIONAL LAW",
        "code": "CML 4108",
        "instructor": "Aram Kerkonian",
        "day_of_week": "Tuesday",
        "start_time": "17:30",
        "end_time": "20:20",
        "room": "57 Louis Pasteur (FTX) 402",
    },
    {
        "name": "GLOBALIZATION AND LAW",
        "code": "CML 4150",
        "instructor": "Errol Mendes",
        "day_of_week": "Tuesday",
        "start_time": "14:30",
        "end_time": "15:50",
        "room": "57 Louis Pasteur (FTX) 315",
    },
    {
        "name": "GLOBALIZATION AND LAW",
        "code": "CML 4150",
        "instructor": "Errol Mendes",
        "day_of_week": "Thursday",
        "start_time": "14:30",
        "end_time": "15:50",
        "room": "57 Louis Pasteur (FTX) 315",
    },
]

@router.post("/seed-classes")
async def seed_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Seed default 3L law school classes"""
    try:
        # Check if classes already exist
        existing_classes = db.query(Class).filter(Class.user_id == current_user.id).all()
        if existing_classes:
            return {
                "message": "Classes already exist",
                "count": len(existing_classes),
                "classes": [{"id": c.id, "name": c.name, "code": c.code} for c in existing_classes],
            }

        # Create classes
        created_classes = []
        for class_data in DEFAULT_CLASSES:
            new_class = Class(
                user_id=current_user.id,
                name=class_data["name"],
                code=class_data["code"],
                instructor=class_data["instructor"],
                day_of_week=class_data.get("day_of_week"),
                start_time=class_data.get("start_time"),
                end_time=class_data.get("end_time"),
                room=class_data.get("room"),
                color="powder-petal",
            )
            db.add(new_class)
            db.flush()
            created_classes.append({
                "id": new_class.id,
                "name": new_class.name,
                "code": new_class.code,
                "instructor": new_class.instructor,
                "day_of_week": new_class.day_of_week,
                "time": f"{new_class.start_time} - {new_class.end_time}",
            })

        db.commit()
        return {
            "message": "Classes created successfully",
            "count": len(created_classes),
            "classes": created_classes,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to seed classes: {str(e)}")

@router.get("/status")
async def setup_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check setup status"""
    classes_count = db.query(Class).filter(Class.user_id == current_user.id).count()
    return {
        "user": current_user.username,
        "classes_count": classes_count,
        "is_setup": classes_count > 0,
    }
