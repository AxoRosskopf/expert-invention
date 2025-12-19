from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime

class Activity(BaseModel):
    id: str
    category: str
    title: str
    desc: str
    date: datetime
    location: str
    coordinates: List[float]
    value: Optional[float] = None
    url: Optional[str] = None

