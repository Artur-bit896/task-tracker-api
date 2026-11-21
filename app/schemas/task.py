from enum import Enum

from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.todo

    @field_validator("title")
    @classmethod
    def clean_title_validating(cls, value):
        clean_title = value.strip()
        if clean_title == "":
            raise ValueError(
                "Это название не может быть использовано так как состоит только из пробелов"
            )
        return clean_title


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200, min_length=5)
    description: str | None = None
    status: TaskStatus | None = None

    @field_validator("title")
    @classmethod
    def clean_title_validating(cls, value):
        if value is None:
            return value
        clean_title = value.strip()
        if clean_title == "":
            raise ValueError(
                "Это название не может быть использовано так как состоит только из пробелов"
            )
        return clean_title
