from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    command: str = Field(..., min_length=3, max_length=100)
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
    tasks: list[TaskResponse]
    page: int = 1
    total_pages: int = 1
    total_tasks: int = 0
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
