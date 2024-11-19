

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False

tasks = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to the TODO App API"}

@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")