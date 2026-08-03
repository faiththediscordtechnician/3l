from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    classes = relationship("Class", back_populates="user", cascade="all, delete-orphan")
    todos = relationship("TodoItem", back_populates="user", cascade="all, delete-orphan")

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    code = Column(String)
    instructor = Column(String)
    notes = Column(Text)
    color = Column(String, default="powder-petal")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="classes")
    readings = relationship("Reading", back_populates="class_obj", cascade="all, delete-orphan")
    todos = relationship("TodoItem", back_populates="class_obj")

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    title = Column(String, index=True)
    source = Column(String)
    assigned_date = Column(DateTime)
    due_date = Column(DateTime, index=True)
    status = Column(String, default="to_read")  # to_read, reading, completed
    pages_total = Column(Integer)
    pages_read = Column(Integer, default=0)
    reading_time_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class_obj = relationship("Class", back_populates="readings")
    notes = relationship("Note", back_populates="reading", cascade="all, delete-orphan")
    annotations = relationship("Annotation", back_populates="reading", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    reading_id = Column(Integer, ForeignKey("readings.id"))
    title = Column(String)
    content = Column(Text)  # RTF content
    tags = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reading = relationship("Reading", back_populates="notes")

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    reading_id = Column(Integer, ForeignKey("readings.id"))
    text = Column(String)
    highlight_color = Column(String, default="yellow")
    page_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    reading = relationship("Reading", back_populates="annotations")

class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    title = Column(String, index=True)
    description = Column(Text)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # low, medium, high
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="todos")
    class_obj = relationship("Class", back_populates="todos")
