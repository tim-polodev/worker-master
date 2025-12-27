import math
from typing import Literal

from fastapi import APIRouter, Body, Depends, Query, Request, Response, status
from pymongo.database import Database

from config import settings
from config.ratelimiter import limiter
from dependencies import get_db
from models.tasks import TaskCreate, TaskListResponse, TaskResponse
from services import TasksService

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.REQUEST_LIMITER)
async def create_task(
    request: Request, task: TaskCreate = Body(...), db: Database = Depends(get_db)
):
    tasks_service = TasksService(db)
    new_task = tasks_service.add_task(task)
    return new_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.REQUEST_LIMITER)
async def delete_task(request: Request, task_id: str, db: Database = Depends(get_db)):
    tasks_service = TasksService(db)
    task = tasks_service.get_task_by_id(task_id)
    if not task:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    tasks_service.remove_task_by_id(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/tasks", response_model=TaskListResponse)
@limiter.limit(settings.REQUEST_LIMITER)
async def get_tasks(
    request: Request,
    limit: int = Query(default=10, ge=1, description="Number of tasks to retrieve per page"),
    page: int = Query(default=1, ge=1, description="Page number"),
    sort_by: str = Query(default="created_at", description="Sorted field"),
    sort_direction: Literal["asc", "desc"] = Query(default="desc", description="Sort direction"),
    db: Database = Depends(get_db),
):
    skip_val = (page - 1) * limit
    mongo_sort = -1 if sort_direction == "desc" else 1
    tasks_service = TasksService(db)
    tasks_list = tasks_service.get_tasks(
        limit=limit, sort_by=sort_by, sort_direction=mongo_sort, skip=skip_val
    )
    total_tasks = tasks_list.get("total_tasks", 0)
    total_pages = math.ceil(total_tasks / limit) if limit > 0 else 0
    return TaskListResponse(
        data=tasks_list.get("tasks", []),
        page=page,
        total_pages=total_pages,
        total_tasks=total_tasks,
    )
