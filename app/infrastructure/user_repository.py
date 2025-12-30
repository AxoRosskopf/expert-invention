from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.infrastructure.models import UserModel, ActivityModel
from app.domain.schemas import User, Activity
from typing import List

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_or_create_activity(self, activity: Activity) -> ActivityModel:
        statement = select(ActivityModel).where(ActivityModel.guid == activity.guid)
        result = await self.db.execute(statement)
        db_activity = result.scalars().first()

        if not db_activity:
            db_activity = ActivityModel(
                guid = activity.guid,
                category = activity.category,
                title = activity.title,
                desc = activity.desc,
                date = activity.date.replace(tzinfo=None) if activity.date else None,
                location = activity.location,
                value=str(activity.value),
                phone = None,
                url = activity.url,
            )
        return db_activity




    async def get_all_users(self) -> List[UserModel]:
        result = await self.db.execute(
            select(UserModel).options(
                selectinload(UserModel.activities),
                selectinload(UserModel.saved_activities)
                )
        )
        return result.scalars().unique().all()
    

    async def create_user(self, user: User) -> UserModel:
        statement = select(UserModel).options(
            selectinload(UserModel.activities),
            selectinload(UserModel.saved_activities)
        ).where(UserModel.guid == user.guid)
        
        result = await self.db.execute(statement)
        db_user = result.scalars().first()

        if not db_user:
            db_user = UserModel(guid=user.guid)
            self.db.add(db_user)
            db_user.activities = []
            db_user.saved_activities = []
        
        activities_to_process = []
        if user.activities:
            for act_schema in user.activities:
                db_activity = await self._get_or_create_activity(act_schema)
                activities_to_process.append(db_activity)
        
        saved_activities_to_process = []
        if user.saved_activities:
            for act_schema in user.saved_activities:
                db_activity = await self._get_or_create_activity(act_schema)
                saved_activities_to_process.append(db_activity)

        if activities_to_process:
            current_ids = {a.guid for a in db_user.activities}
            for db_act in activities_to_process:
                if db_act.guid not in current_ids:
                    db_user.activities.append(db_act)
                    current_ids.add(db_act.guid)

        if saved_activities_to_process:
            current_saved_ids = {a.guid for a in db_user.saved_activities}
            for db_act in saved_activities_to_process:
                if db_act.guid not in current_saved_ids:
                    db_user.saved_activities.append(db_act)
                    current_saved_ids.add(db_act.guid)
        
        await self.db.commit()


        result_refresh = await self.db.execute(
             select(UserModel)
             .options(
                 selectinload(UserModel.activities),
                 selectinload(UserModel.saved_activities))
             .where(UserModel.guid == db_user.guid)
        )
        return result_refresh.scalars().first()
    


    async def get_user(self, guid: str) -> UserModel:
        result = await self.db.execute(
            select(UserModel)
            .options(selectinload(UserModel.activities), selectinload(UserModel.saved_activities))
            .where(UserModel.guid == guid)
        )
        return result.scalars().first()
    
    
    async def add_activity(self, guid_user: str, activity: Activity) -> UserModel:
        stmt = select(UserModel).options(selectinload(UserModel.activities)).where(UserModel.guid == guid_user)
        result = await self.db.execute(stmt)
        db_user = result.scalars().first()

        if not db_user: return None
        
        db_activity = await self._get_or_create_activity(activity)
        
        existing_ids = [a.guid for a in db_user.activities]
        if db_activity.guid not in existing_ids:
            db_user.activities.append(db_activity)
            await self.db.commit()
            await self.db.refresh(db_user)

        return db_user
    

    async def add_saved_activity(self, guid_user: str, activity: Activity) -> UserModel:
        stmt = select(UserModel).options(selectinload(UserModel.saved_activities)).where(UserModel.guid == guid_user)
        result = await self.db.execute(stmt)
        db_user = result.scalars().first()

        if not db_user: return None
        
        db_activity = await self._get_or_create_activity(activity)
        
        existing_ids = [a.guid for a in db_user.saved_activities]
        if db_activity.guid not in existing_ids:
            db_user.saved_activities.append(db_activity)
            await self.db.commit()
            await self.db.refresh(db_user)
        
        return db_user

    async def get_saved_activities(self, guid: str) -> List[ActivityModel]:
        stmt = select(UserModel).options(selectinload(UserModel.saved_activities)).where(UserModel.guid == guid)
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if user:
            return user.saved_activities
        return []
    

    async def delete_saved_activity(self, guid_user: str, guid_activity: str) -> UserModel:
        stmt = select(UserModel).options(selectinload(UserModel.saved_activities)).where(UserModel.guid == guid_user)
        result = await self.db.execute(stmt)
        db_user = result.scalars().first()

        if not db_user: return None
        
        activity_to_remove = next((act for act in db_user.saved_activities if act.guid == guid_activity), None)

        if activity_to_remove:
            db_user.saved_activities.remove(activity_to_remove)
            await self.db.commit()
            await self.db.refresh(db_user)
        return db_user 