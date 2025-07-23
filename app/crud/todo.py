from sqlalchemy.orm import Session
from app.models.todo import Items
from app.schemas.models import TodoItemCreate, TodoUpdate
from fastapi import FastAPI,HTTPException,Request,Form

def get_todos(db: Session):
    return db.query(Items).all()

def get_todo(db: Session, todo_id:int):
    return db.query(Items).filter(Items.id == todo_id).first()

def create_todo(db: Session, todo: TodoItemCreate):
    db_todo = Items(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id:int):
    db_todo = db.query(Items).filter(Items.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False

def update_todo(db:Session, todo_id:int, update_item:TodoUpdate):
    db_todo = db.query(Items).filter(Items.id == todo_id).first()
    if db_todo:
        update_data = update_item.model_dump(exclude_unset=True)
        for field,value in update_data.items():
            setattr(db_todo,field,value)
        db.commit()
        db.refresh(db_todo)
    return db_todo