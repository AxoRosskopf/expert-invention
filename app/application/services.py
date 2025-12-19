from typing import List
from app.domain.schemas import Activity
from app.infrastructure.notion_repository import NotionRepository

class ActivityService:
    def __init__(self, repository: NotionRepository):
        self.repository = repository

    async def get_activities(self)-> List[Activity]:
        activities = await self.repository.get_all_activities()
        return activities