from fastapi import FastAPI
from app.api.v1.tasks import router as tasks_router


app = FastAPI()
app.include_router(tasks_router)


@app.get("/")
def home():
    return "Hello World"