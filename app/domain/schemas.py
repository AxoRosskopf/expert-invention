from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime
from enum import Enum

class InteractionTypeEnum(str, Enum):
    VIEW = "view"
    IGNORE = "ignore"
    CLICK = "click"
    SAVE = "save"

class InteractionBase(BaseModel):
    activity_guid: str
    action: InteractionTypeEnum

class InteractionCreate(InteractionBase):
    pass

class InteractionRead(InteractionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class Activity(BaseModel):
    guid: str
    category: str
    title: str
    desc: str
    date: datetime
    location: str
    coordinates: List[float]
    value: Optional[float] = None
    url: Optional[str] = None

    class Config:
        from_attributes = True

class User(BaseModel):
    guid: str
    saved_activities: List[Activity] = []
    class Config:
        from_attributes = True