#!/usr/bin/env python3
"""
Seed script to populate classes for the 3L Academic Hub
Run this after setting up the database
"""

from database import SessionLocal
from models import User, Class

CLASSES = [
    {
        "name": "MEDIATION THEORY AND PRACTICE",
        "code": "CML 2320",
        "instructor": "Emilia Péch",
        "notes": "Wed 5:30PM - 8:20PM | Room: 120 University (FSS) 14001",
    },
    {
        "name": "LABOUR LAW I",
        "code": "CML 3233",
        "instructor": "Ravi A. Malhotra",
        "notes": "Mon 2:30PM - 3:50PM, Wed 1:00PM - 2:20PM | Room: 57 Louis Pasteur (FTX) 137",
    },
    {
        "name": "STUDIES IN PUBLIC LAW",
        "code": "CML 4104",
        "instructor": "Andres Drew",
        "notes": "Mon 4:00PM - 6:50PM | Room: 57 Louis Pasteur (FTX) 413",
    },
    {
        "name": "STUDIES IN INTERNATIONAL LAW",
        "code": "CML 4108",
        "instructor": "Aram Kerkonian",
        "notes": "Tue 5:30PM - 8:20PM | Room: 57 Louis Pasteur (FTX) 402",
    },
    {
        "name": "GLOBALIZATION AND LAW",
        "code": "CML 4150",
        "instructor": "Errol Mendes",
        "notes": "Tue 2:30PM - 3:50PM, Thu 2:30PM - 3:50PM | Room: 57 Louis Pasteur (FTX) 315",
    },
]

def seed_classes():
    db = SessionLocal()
    try:
        # Get the marie user
        marie_user = db.query(User).filter(User.username == "marie").first()
        if not marie_user:
            print("✗ Marie user not found. Please create the marie user first.")
            return

        # Check if classes already exist
        existing_classes = db.query(Class).filter(Class.user_id == marie_user.id).count()
        if existing_classes > 0:
            print(f"✓ {existing_classes} classes already exist for marie")
            print("Skipping seed (to re-seed, delete existing classes first)")
            return

        # Create classes
        for class_data in CLASSES:
            new_class = Class(
                user_id=marie_user.id,
                name=class_data["name"],
                code=class_data["code"],
                instructor=class_data["instructor"],
                notes=class_data["notes"],
                color="powder-petal",
            )
            db.add(new_class)
            print(f"✓ Created: {class_data['code']} - {class_data['name']}")

        db.commit()
        print(f"\n✓ Successfully seeded {len(CLASSES)} classes!")
        print("Your 3L courses are ready to go! 🎓")

    except Exception as e:
        print(f"✗ Error seeding classes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_classes()
