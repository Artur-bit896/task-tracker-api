from app.db.session import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskStatus, TaskUpdate


def create_task(task: TaskCreate) -> Task:
    db = SessionLocal()
    try:
        task_dict = task.model_dump()
        task_dict["status"] = task_dict["status"].value

        new_task = Task(**task_dict)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task
    finally:
        db.close()


def get_tasks(status: TaskStatus | None = None) -> list[Task]:
    db = SessionLocal()
    try:
        if status is None:
            return db.query(Task).all()
        else:
            return db.query(Task).filter(Task.status == status.value).all()
    finally:
        db.close()


def get_task_by_id(task_id: int) -> Task | None:
    db = SessionLocal()
    try:
        return db.query(Task).filter(Task.id == task_id).first()
    finally:
        db.close()


def update_task(task_id: int, task_data: TaskUpdate) -> None | Task:
    db = SessionLocal()
    try:
        taski = db.query(Task).filter(Task.id == task_id).first()
        if taski is None:
            return None
        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(taski, key, value)
        db.commit()
        db.refresh(taski)
        return taski
    finally:
        db.close()


def delete_task(task_id: int) -> Task | None:
    db = SessionLocal()
    try:
        taski = db.query(Task).filter(Task.id == task_id).first()
        if taski is None:
            return None
        db.delete(taski)
        db.commit()
        return taski
    finally:
        db.close()
