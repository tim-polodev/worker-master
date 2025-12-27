from datetime import datetime
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class FargateTaskConfig(BaseModel):
    type: Literal["fargate-ecs"] = Field(default="fargate-ecs", description="Task type")
    cpu: int = Field(default=256, ge=256, le=1024, description="CPU units for the task")
    memory: int = Field(default=100, ge=100, le=2048, description="Memory (in MiB) for the task")
    cluster: str = Field(default="default", description="ECS cluster name")
    task_definition: str = Field(default="default", description="ECS task definition")


class ApiTaskConfig(BaseModel):
    type: Literal["api"] = Field(default="api", description="Task type")
    method: str = Field(default="GET", description="HTTP method")
    url: str = Field(default="", description="URL to call")
    headers: dict = Field(default={}, description="HTTP headers")
    body: dict = Field(default={}, description="HTTP body")


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Task title")
    config: Annotated[Union[FargateTaskConfig, ApiTaskConfig], Field(discriminator="type")] = Field(
        ..., description="Task configuration (depends on task type)"
    )
    type: Literal["fargate-ecs", "api", "scheduled"] = Field(..., description="Type of task")
    description: Optional[str] = None
    recipient_emails: Optional[list[EmailStr]] = []


class TaskCreate(TaskBase):
    """Schema for creating a task (client input)"""

    pass


class TaskResponse(TaskBase):
    """Schema for reading a task (API output)"""

    id: PyObjectId = Field(alias="_id")  # Map _id to id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending")
    retry_count: int = 0
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class TaskListResponse(BaseModel):
    data: list[TaskResponse]
    page: int = 1
    total_pages: int = 1
    total_tasks: int = 0
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
