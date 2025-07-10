from fastapi import FastAPI,HTTPException,Request
from models import TodoItem, TodoItemCreate, TodoUpdate
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

todo_list = []
next_id = 1


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("message.html", {"request": request, "todo_list": todo_list })


@app.get("/todos/{id}", response_model=TodoItem)
async def show_todos(id: int,request: Request):
    for todo in todo_list:
        if todo.id == id:
            return templates.TemplateResponse("message.html", {"request": request, "item": todo })
    raise HTTPException(status_code = 404,\
                        detail = f"item number {id} not found")
"""
@app.get("/todos")
def show_todos():
    return {"message" : "your todos list" , "list" : todo_list}
"""
@app.delete("/todos/{id}")
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
def replace_item(id:int,update_item: TodoUpdate):
    for item in todo_list:
        if item.id == id:
            updated_data = item.model_dump()
            update_dict = update_item.model_dump(exclude_unset=True)
            #update_item = TodoItem(id=item.id,**update_item.model_dump(ex))
            updated_data.update(update_dict)
            updated_todo = TodoItem(**updated_data)
            todo_list[todo_list.index(item)] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404,detail='To-do item not found')


@app.post('/todos/',response_model=TodoItem)
async def create_todo(item: TodoItemCreate):
    global next_id
    todo = TodoItem(id=next_id, **item.model_dump())
    next_id += 1
    print(f"Returning: {todo.model_dump()}")
    todo_list.append(todo)
    return todo