from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel,model_validator

class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TodoItemBase(BaseModel):
    title: str
    status: StatusEnum = StatusEnum.pending
    start_date: datetime = datetime.now()
    end_date: Optional[datetime] = None
    description: Optional[str] = None
"""
    @model_validator(mode='after')
    def check_dates(self):
        if self.start_date > self.end_date:
            raise ValueError('end_date must be after start_date')
        return self
"""
class TodoItemCreate(TodoItemBase):
    pass

class TodoUpdate(BaseModel):
    title : Optional[str] = None
    status: Optional[StatusEnum] = None
    start_date: Optional[datetime] = None
    
class TodoResponse(TodoItemBase):
    id:int
    status: StatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TodoStatusUpdate(BaseModel):
    status: StatusEnum