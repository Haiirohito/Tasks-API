# API routes

from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongo import get_collection
from app.models.task import TaskCreate, TaskInDB, TaskUpdate
from app.crud import task_crud

router = APIRouter()


@router.get("/", response_model=list[TaskInDB])
async def list_tasks(collection=Depends(get_collection)):
    tasks = await task_crud.get_all_tasks(collection)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return tasks


@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str, collection=Depends(get_collection)):
    task = await task_crud.get_task_by_id(collection, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not found")

    task["_id"] = str(task["_id"])
    return task


# @router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
# async def create(task: TaskCreate, collection=Depends(get_collection)):
#     return await task_crud.create_task(collection, task.dict())


@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
async def create(task: TaskCreate, collection=Depends(get_collection)):
    task_dict = task.model_dump()
    result = await collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    return TaskInDB(**task_dict)


@router.put("/{task_id}", response_model=TaskInDB)
async def update(task_id: str, task: TaskUpdate, collection=Depends(get_collection)):
    existing = await task_crud.get_task_by_id(collection, task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task Not found")

    updated = await task_crud.update_task(
        collection, task_id, task.dict(exclude_unset=True)
    )

    if updated and "_id" in updated:
        updated["_id"] = str(updated["_id"])

    return TaskInDB(**updated)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: str, collection=Depends(get_collection)):
    success = await task_crud.delete_task(collection, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task Not found")
