from fastapi import FastAPI
from models import TodoItem

app = FastAPI()

todo_list = []

@app.get("/")
def read_root():
    return {"message": "Welcome to my To-Do list"}

@app.get("/todos")
def show_todos():
    return {"message": "your todos list", "list" : todo_list}
@app.post('/todos')
def create_todo(item: TodoItem):
    todo_list.append(item)
    return {'message': 'todo item created','item': item}