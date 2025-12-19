from fastapi import APIRouter, Depends
from typing import List
from app.domain.schemas import Activity
from app.application.services import ActivityService
from app.api.dependencies import get_service
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

