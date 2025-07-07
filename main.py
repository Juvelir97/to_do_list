from fastapi import FastAPI,HTTPException
from models import TodoItem, TodoItemCreate

app = FastAPI()

todo_list = []
next_id = 1


@app.get("/")
async def read_root():
    return {"message": "Welcome to my To-Do list"}


@app.get("/todos/{id}", response_model=TodoItem)
async def show_todos(id: int):
    for todo in todo_list:
        if todo.id == id:
            return todo
    raise HTTPException(status_code = 404,\
                        detail = f"item number {id} not found")

@app.get("/todos")
def show_todos():
    return {"message" : "your todos list" , "list" : todo_list}

@app.delete("/todos/delete/{id}")
def delete_item(id : int):
    if id < 0:
        raise ValueError("Id cannot be negative")
    else:
        for index,todo in enumerate(todo_list):
            if todo.id == id:
                removed_item = todo_list.pop(index)
                return removed_item.title
        
        raise HTTPException(status_code=404,detail=f"To-do item not found {id} - {todo.id}")

@app.put("/todos/{id}", response_model=TodoItem)
def replace_item(id:int,update_item: TodoItem):
    for index,item in enumerate(todo_list):
        if item.id == id:
            todo_list[index] = update_item
            return update_item
    raise HTTPException(status_code=404,detail='To-do item not found')


@app.post('/todos/',response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    global next_id
    todo = TodoItem(id=next_id, **item.model_dump())
    next_id += 1
    print(f"Returning: {todo.model_dump()}")
    todo_list.append(todo)
    return todo