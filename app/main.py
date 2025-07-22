from fastapi import FastAPI,HTTPException,Request,Form
#from app.models import TodoItem, TodoItemCreate, TodoUpdate
from app.db import engine
from app.api import routes
from app.models import todo

todo.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routes.router)
