# API routes

from fastapi import APIRouter, Depends
from app.db.mongo import get_collection
from app.models.task import TaskCreate, TaskInDB
from app.crud.task_crud import get_all_tasks, create_task

router = APIRouter()

@router.get("/", response_model=list[TaskInDB])
async def list_tasks(collection=Depends(get_collection)):
    tasks = await get_all_tasks(collection)
    return tasks

@router.post("/", response_model=TaskInDB)
async def add_task(task: TaskCreate, collection=Depends(get_collection)):
    new_task = await create_task(collection, task.dict())
    return new_task