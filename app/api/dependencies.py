from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.notion_repository import NotionRepository
from app.infrastructure.user_repository import UserRepository
from app.application.services import ActivityService, UserService
from app.core.database import get_db


def get_repository() -> NotionRepository:
    return NotionRepository()

def get_service(repo: NotionRepository = Depends(get_repository)):
    return ActivityService(repo)

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)