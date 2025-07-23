from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends,Request, HTTPException,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from sqlalchemy.orm import Session
from app.schemas.models import TodoItemCreate
from app.crud import todo as crud_todo
from app.dependencies.db_depends import get_db



templates = Jinja2Templates(directory='app/templates')


#todo_list = []
#next_id = 1

router = APIRouter(tags=["todos"])

@router.get("/",response_class=HTMLResponse)
async def read_root(request: Request,db : Session = Depends(get_db)):
    todo_list = crud_todo.get_todos(db)
    return templates.TemplateResponse("message.html", {"request": request, "todo_list": todo_list })


@router.get("/todos/{id}", response_class=HTMLResponse)
async def show_todos(id: int,request: Request,db: Session = Depends(get_db)):
    todo = crud_todo.get_todo(db,id)
    if not todo:
            raise HTTPException(status_code = 404,\
                        detail = f"item number {id} not found")
    
    return templates.TemplateResponse("message.html", {"request": request, "item": todo })
    

@router.delete("/todos/{id}")
def delete_item(id : int,db:Session=Depends(get_db)):
    if id < 0:
        raise ValueError("Id cannot be negative")
    else:
        if crud_todo.delete_todo(db,id):
                return {"message": f"Item {id} has been deleted"}
        raise HTTPException(status_code=404,detail=f"To-do item with id {id} not found")
"""
@router.put("/todos/{id}", response_model=TodoItem)
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

"""
@router.post('/',response_model=TodoItemCreate)
async def create_todo(title: str = Form(),description: str = Form(),db:Session=Depends(get_db)):
    todo = TodoItemCreate(title=title, description=description)
    crud_todo.create_todo(db,todo)
    return RedirectResponse(url="/",status_code=303) 
#templates.TemplateResponse("message.html", {"request": request, "todo_list": todo})