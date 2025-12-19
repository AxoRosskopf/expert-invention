from notion_client import Client
from app.core.config import settings
from app.domain.schemas import Activity
from typing import List
from app.core.utils import from_map_url_to_coordinates



class NotionRepository:
    def __init__(self):
        self.client = Client(auth=settings.NOTION_TOKEN)
    
    async def get_all_activities(self)-> List[Activity]:
        try:
            response = self.client.data_sources.query(data_source_id=settings.DATABASE_ID)
            activities = []

            for page in  response.get("results",[]):
                props = page.get("properties",{})

                def get_id(): return page.get("id")
                def get_title(p): return p.get("title", [{}])[0].get("plain_text", "Sin título") if p.get("title") else "Sin título"
                def get_select(p): return p.get("select", {}).get("name", "General") if p.get("select") else "General"
                def get_text(p): return p.get("rich_text", [{}])[0].get("plain_text", "") if p.get("rich_text") else ""
                def get_date(p): return p.get("date", {}).get("start") if p.get("date") else None
                def get_number(p): return p.get("number")
                def get_url(p): return p.get("url")

                activity = Activity(
                    id=get_id(),
                    title=get_title(props.get("event_name", {})),
                    category=get_select(props.get("category", {})),
                    desc=get_text(props.get("description", {})),
                    date=get_date(props.get("event_date", {})) or datetime.now(),
                    location=get_text(props.get("location", {})) or "No especificada",
                    coordinates=from_map_url_to_coordinates(get_url(props.get("url_location", {}))),
                    value=get_number(props.get("cost", {})),
                    url=get_url(props.get("action", {}))
                )
                activities.append(activity)

            return activities
        
        except Exception as e:
            print(f"Error fetching activities from Notion: {e}")
            return []