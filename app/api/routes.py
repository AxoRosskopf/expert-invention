from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.domain.schemas import Activity, User, InteractionTypeEnum, InteractionRead
from app.application.services import ActivityService, UserService
from app.api.dependencies import get_service, get_user_service
from app.core.utils import haversine_distance

router = APIRouter()

@router.get('/activities', response_model=List[Activity])
async def read_activities(service: ActivityService = Depends(get_service)):
    activities = await service.get_activities()
    return activities

@router.get('/activities/{category}', response_model=List[Activity])
async def read_activities_by_category(category: str, service: ActivityService = Depends(get_service)):
    activities = await service.get_activities()
    filtered_activities = [activity for activity in activities if activity.category.lower() == category.lower()]
    return filtered_activities

@router.get('/activity/categories', response_model=List[str])
async def read_activity_categories(service: ActivityService = Depends(get_service)):
    activities = await service.get_activities()
    categories = list(set(activity.category for activity in activities))
    return categories


@router.get('/nearby-activities/{lat}/{lon}', response_model=List[Activity])
async def read_nearby_activities(lat: float, lon: float, service: ActivityService = Depends(get_service)):
    activities = await service.get_activities()
    actual_location: List[float] = [lat, lon]
    aux = []
    
    for activity in activities:
        distance = haversine_distance(actual_location, activity.coordinates)
        aux.append((distance, activity))
    
    aux.sort(key=lambda x: x[0])
    nearby_activities = [item[1] for item in aux]
    return nearby_activities



# User endpoints

@router.post('/users', response_model=User)
async def create_user(user: User, service: UserService = Depends(get_user_service)):
    create_user = await service.create_user(user)
    return create_user


@router.get('/users', response_model=List[User])
async def read_users(service: UserService = Depends(get_user_service)):
    users = await service.get_users()
    return users

@router.get('/users/{guid}', response_model=User)
async def read_user(guid: str, service: UserService = Depends(get_user_service)):
    user = await service.get_user_by_id(guid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@router.post('/users/{guid}/interactions', response_model=User)
async def create_log_interaction(guid, activity: Activity, action: InteractionTypeEnum, service: UserService = Depends(get_user_service)):
    user = await service.log_interaction(guid, activity, action)
    return user

@router.get('/users/{guid}/interactions', response_model=List[Dict[str, Any]])
async def read_log_interactions(guid, service: UserService = Depends(get_user_service)):
    interactions = await service.get_log_interactions(guid)
    return interactions

@router.get('/users/{guid}/saved_activities', response_model=List[Activity])
async def get_saved_activities(guid,service : UserService = Depends(get_user_service)):
    activities = await service.get_saved_activities(guid)
    return activities

@router.delete('/users/{guid_user}/saved_activities/{guid_activity}', response_model=User)
async def delete_saved_activity(guid_user, guid_activity, service : UserService = Depends(get_user_service)):
    user = await service.delete_saved_activity(guid_user, guid_activity)
    if not user:
        raise HTTPException(status_code=404, detail="User or Activity not found")
    return user

