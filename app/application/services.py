from typing import List
from app.domain.schemas import Activity, User
from app.infrastructure.notion_repository import NotionRepository
from app.infrastructure.user_repository import UserRepository

class ActivityService:
    def __init__(self, repository: NotionRepository):
        self.repository = repository

    async def get_activities(self)-> List[Activity]:
        return await self.repository.get_all_activities()

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository =  repository
    
    async def get_users(self)-> List[User]:
        return await self.repository.get_all_users()
    
    async def create_user(self, user: User) -> User:
        return await self.repository.create_user(user)
    
    async def get_user_by_id(self, guid: str) -> User:
        return await self.repository.get_user(guid)
    
    
    
    # NEW METHODZ

    async def add_activity(self, guid_user: str,activity: Activity) -> User:
        return await self.repository.add_activity(guid_user,activity)
    
    async def add_saved_activity(self, guid_user:str ,activity: Activity) -> User:
        return await self.repository.add_saved_activity(guid_user, activity)
    
    async def get_saved_activities(self, guid: str) -> List[Activity]:
        return await self.repository.get_saved_activities(guid)
    
    async def delete_saved_activity(self, guid__user: str, guid_activity: str) -> User:
        return await self.repository.delete_saved_activity(guid__user, guid_activity)

