from pydantic import BaseModel, Field
from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.todo

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
