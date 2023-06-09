from fastapi import FastAPI, HTTPException, Response, status, Body
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import Todo
from backend.database import create_item, \
    delete_item, \
    update_item, \
    get_item_by_title, \
    get_all_todos

app = FastAPI()


@app.get('/api/get_todos')
async def get_todo():
    todos = await get_all_todos()
    if not todos:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return todos


@app.get('/api/get_todo/{title}', response_model=Todo)
async def get_todo(title: str):
    todo = await get_item_by_title(title)
    if not todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'no item with {title} that title')
    return todo


@app.post('/api/create_todo/')
async def create_todo(todo_data: Todo):
    await create_item(todo_data.dict())
    return Response(status_code=status.HTTP_201_CREATED)


@app.put('/api/full_update_todo/{title}', response_model=Todo)
async def full_update_todo(title: str, desc: str = Body(...)):
    item = await update_item(title, desc)
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return item


@app.delete('/api/delete{title}')
async def get_todo(title: str):
    await delete_item(title)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
