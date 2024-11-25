from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get API Key from environment variables
API_KEY = os.getenv("LAB_API_KEY")

# API key dependency
def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key.")
    return api_key

# Shared Task Database
task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

# Task Model
class Task(BaseModel):
    task_title: str
    task_desc: Optional[str] = ""
    is_finished: bool = False

# Version 1 Router
apiv1 = APIRouter()

@apiv1.get("/file/{task_id}", tags=["v1"])
def get_task(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return JSONResponse(status_code=200, content={"message": "Task retrieved successfully.", "task": task})

@apiv1.post("/file", tags=["v1"])
def create_task(task: Task, api_key: str = Depends(verify_api_key)):
    task_id = len(task_db) + 1
    new_task = task.dict()
    new_task["task_id"] = task_id
    task_db.append(new_task)
    return JSONResponse(status_code=201, content={"message": "Task successfully created.", "task": new_task})

@apiv1.patch("/file/{task_id}", tags=["v1"])
def update_task(task_id: int, task: Task, api_key: str = Depends(verify_api_key)):
    task_entry = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task_entry:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_entry.update(task.dict())
    return JSONResponse(status_code=204, content={"message": "Task successfully updated."})

@apiv1.delete("/file/{task_id}", tags=["v1"])
def delete_task(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_db.remove(task)
    return JSONResponse(status_code=204, content={"message": f"Task with ID {task_id} successfully deleted."})

# Version 2 Router with the same functionality for demonstration
apiv2 = APIRouter()

@apiv2.get("/file/{task_id}", tags=["v2"])
def get_task_v2(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return JSONResponse(status_code=200, content={"message": "Task retrieved successfully.", "task": task})

@apiv2.post("/file", tags=["v2"])
def create_task_v2(task: Task, api_key: str = Depends(verify_api_key)):
    task_id = len(task_db) + 1
    new_task = task.dict()
    new_task["task_id"] = task_id
    task_db.append(new_task)
    return JSONResponse(status_code=201, content={"message": "Task successfully created.", "task": new_task})

@apiv2.patch("/file/{task_id}", tags=["v2"])
def update_task_v2(task_id: int, task: Task, api_key: str = Depends(verify_api_key)):
    task_entry = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task_entry:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_entry.update(task.dict())
    return JSONResponse(status_code=204, content={"message": "Task successfully updated."})

@apiv2.delete("/file/{task_id}", tags=["v2"])
def delete_task_v2(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_db.remove(task)
    return JSONResponse(status_code=204, content={"message": f"Task with ID {task_id} successfully deleted."})

# Register Routers
app.include_router(apiv1, prefix="/v1")
app.include_router(apiv2, prefix="/v2")
