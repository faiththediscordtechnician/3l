from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import TodoItem, User, Class
from schemas import TodoItemCreate, TodoItemResponse
from auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoItemResponse)
def create_todo(todo_data: TodoItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if todo_data.class_id:
        db_class = db.query(Class).filter(
            Class.id == todo_data.class_id,
            Class.user_id == current_user.id
        ).first()
        if not db_class:
            raise HTTPException(status_code=404, detail="Class not found")

    db_todo = TodoItem(
        user_id=current_user.id,
        class_id=todo_data.class_id,
        title=todo_data.title,
        description=todo_data.description,
        due_date=todo_data.due_date,
        completed=todo_data.completed,
        priority=todo_data.priority
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=list[TodoItemResponse])
def get_todos(class_id: int = None, completed: bool = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(TodoItem).filter(TodoItem.user_id == current_user.id)
    if class_id:
        query = query.filter(TodoItem.class_id == class_id)
    if completed is not None:
        query = query.filter(TodoItem.completed == completed)
    return query.all()

@router.get("/{todo_id}", response_model=TodoItemResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(TodoItem).filter(
        TodoItem.id == todo_id,
        TodoItem.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/{todo_id}", response_model=TodoItemResponse)
def update_todo(todo_id: int, todo_data: TodoItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(TodoItem).filter(
        TodoItem.id == todo_id,
        TodoItem.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.title = todo_data.title
    db_todo.description = todo_data.description
    db_todo.due_date = todo_data.due_date
    db_todo.completed = todo_data.completed
    db_todo.priority = todo_data.priority
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.patch("/{todo_id}/toggle", response_model=TodoItemResponse)
def toggle_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(TodoItem).filter(
        TodoItem.id == todo_id,
        TodoItem.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(TodoItem).filter(
        TodoItem.id == todo_id,
        TodoItem.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}
