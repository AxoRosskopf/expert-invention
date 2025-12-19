from fastapi import Depends
from app.infrastructure.notion_repository import NotionRepository
from app.application.services import ActivityService

def get_repository() -> NotionRepository:
    return NotionRepository()

def get_service(repo: NotionRepository = Depends(get_repository)):
    return ActivityService(repo)

