from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 定義任務的資料結構
class Task(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

# 假資料庫（用於存儲任務）
tasks = []

# 查詢所有任務
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# 查詢單一任務
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# 新增任務
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    # 確保 ID 不重複
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

# 更新任務
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# 刪除任務
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
