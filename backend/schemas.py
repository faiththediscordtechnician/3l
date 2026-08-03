from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ClassBase(BaseModel):
    name: str
    code: Optional[str] = None
    instructor: Optional[str] = None
    notes: Optional[str] = None
    color: str = "powder-petal"

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReadingBase(BaseModel):
    title: str
    source: Optional[str] = None
    assigned_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: str = "to_read"
    pages_total: Optional[int] = None

class ReadingCreate(ReadingBase):
    class_id: int

class ReadingResponse(ReadingBase):
    id: int
    class_id: int
    pages_read: int
    reading_time_minutes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str
    tags: Optional[dict] = None

class NoteCreate(NoteBase):
    reading_id: int

class NoteResponse(NoteBase):
    id: int
    reading_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnnotationBase(BaseModel):
    text: str
    highlight_color: str = "yellow"
    page_number: Optional[int] = None

class AnnotationCreate(AnnotationBase):
    reading_id: int

class AnnotationResponse(AnnotationBase):
    id: int
    reading_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TodoItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    priority: str = "medium"

class TodoItemCreate(TodoItemBase):
    class_id: Optional[int] = None

class TodoItemResponse(TodoItemBase):
    id: int
    user_id: int
    class_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
