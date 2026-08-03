from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import sys
import os
from datetime import datetime
from io import BytesIO
import markdown

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import Reading, Note, Class, User
from auth import get_current_user

router = APIRouter(prefix="/export", tags=["export"])

def generate_markdown_content(reading: Reading, notes: list[Note]) -> str:
    content = f"# {reading.title}\n\n"
    content += f"**Source:** {reading.source or 'N/A'}\n\n"
    content += f"**Status:** {reading.status}\n\n"

    if reading.pages_total:
        content += f"**Progress:** {reading.pages_read}/{reading.pages_total} pages\n\n"
    if reading.reading_time_minutes:
        content += f"**Time Spent:** {reading.reading_time_minutes} minutes\n\n"

    if reading.due_date:
        content += f"**Due Date:** {reading.due_date.strftime('%Y-%m-%d')}\n\n"

    content += "## Notes\n\n"
    for note in notes:
        if note.title:
            content += f"### {note.title}\n\n"
        content += f"{note.content}\n\n"
        if note.tags:
            tags = ", ".join([f"`{tag}`" for tag in note.tags.keys()])
            content += f"**Tags:** {tags}\n\n"

    return content

@router.get("/reading/{reading_id}/markdown")
async def export_reading_markdown(
    reading_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    notes = db.query(Note).filter(Note.reading_id == reading_id).all()
    markdown_content = generate_markdown_content(db_reading, notes)

    filename = f"{db_reading.title.replace(' ', '_')}.md"
    return FileResponse(
        BytesIO(markdown_content.encode()),
        media_type="text/markdown",
        filename=filename
    )

@router.get("/class/{class_id}/markdown")
async def export_class_markdown(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_class = db.query(Class).filter(
        Class.id == class_id,
        Class.user_id == current_user.id
    ).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")

    readings = db.query(Reading).filter(Reading.class_id == class_id).all()

    content = f"# {db_class.name}\n\n"
    if db_class.code:
        content += f"**Course Code:** {db_class.code}\n\n"
    if db_class.instructor:
        content += f"**Instructor:** {db_class.instructor}\n\n"
    if db_class.notes:
        content += f"**Notes:** {db_class.notes}\n\n"

    content += "## Readings\n\n"
    for reading in readings:
        notes = db.query(Note).filter(Note.reading_id == reading.id).all()
        content += generate_markdown_content(reading, notes)
        content += "\n---\n\n"

    filename = f"{db_class.name.replace(' ', '_')}_notes.md"
    return FileResponse(
        BytesIO(content.encode()),
        media_type="text/markdown",
        filename=filename
    )

@router.get("/reading/{reading_id}/pdf")
async def export_reading_pdf(
    reading_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch

    db_reading = db.query(Reading).join(Class).filter(
        Reading.id == reading_id,
        Class.user_id == current_user.id
    ).first()
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")

    notes = db.query(Note).filter(Note.reading_id == reading_id).all()

    pdf_filename = f"{db_reading.title.replace(' ', '_')}.pdf"
    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#9d8189'
    )

    story.append(Paragraph(db_reading.title, title_style))
    story.append(Spacer(1, 12))

    info_style = styles['Normal']
    if db_reading.source:
        story.append(Paragraph(f"<b>Source:</b> {db_reading.source}", info_style))
    story.append(Paragraph(f"<b>Status:</b> {db_reading.status}", info_style))

    if db_reading.pages_total:
        story.append(Paragraph(f"<b>Progress:</b> {db_reading.pages_read}/{db_reading.pages_total} pages", info_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Notes", styles['Heading2']))
    story.append(Spacer(1, 6))

    for note in notes:
        if note.title:
            story.append(Paragraph(note.title, styles['Heading3']))
        story.append(Paragraph(note.content, info_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    pdf_buffer.seek(0)

    return FileResponse(
        pdf_buffer,
        media_type="application/pdf",
        filename=pdf_filename
    )
