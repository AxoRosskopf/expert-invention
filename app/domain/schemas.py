from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime

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
    activities: List[Activity] = []
    saved_activities: List[Activity] = []
    class Config:
        from_attributes = True