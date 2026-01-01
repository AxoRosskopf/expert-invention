from typing import List, Dict, Any
from app.domain.schemas import Activity, User, InteractionTypeEnum, InteractionRead
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

    async def log_interaction(
                self, 
                guid_user:str, 
                activity:Activity, 
                action:InteractionTypeEnum
            ) -> User:

        return await self.repository.log_interaction(guid_user,activity,action)
    
    async def get_log_interactions(self, guid: str) -> List[Dict[str, Any]]:
        db_interactions = await self.repository.get_log_interactions(guid)
        return [
                    InteractionRead.model_validate(interaction).model_dump(mode='json') 
                    for interaction in db_interactions
                ]
    async def get_saved_activities(self, guid: str) -> List[Activity]:
        return await self.repository.get_saved_activities(guid)
    
    async def delete_saved_activity(self, guid__user: str, guid_activity: str) -> User:
        return await self.repository.delete_saved_activity(guid__user, guid_activity)

