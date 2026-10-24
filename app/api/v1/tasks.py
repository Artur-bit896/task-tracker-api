from fastapi import APIRouter, HTTPException, Response
from app.schemas.task import TaskCreate, TaskStatus, TaskUpdate
from app.services.task import create_task, get_tasks, get_task_by_id, update_task, delete_task


router = APIRouter()


@router.post("/api/v1/tasks", status_code=201)
def post(task: TaskCreate):
    return create_task(task)

@router.get("/api/v1/tasks")
def get_all_tasks(status: TaskStatus | None = None):
    return get_tasks(status)

@router.get("/api/v1/tasks/{task_id}")
def get(task_id: int):
    i = get_task_by_id(task_id)
    if i is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return i

@router.patch("/api/v1/tasks/{task_id}")
def patch(task_id:int, data:TaskUpdate):
    y = update_task(task_id, data)
    if y is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return y

@router.delete("/api/v1/tasks/{task_id}")
def delete(task_id: int):
    o = delete_task(task_id)
    if o is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)