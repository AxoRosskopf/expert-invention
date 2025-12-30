from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.utils import from_map_url_to_coordinates

class UserModel(Base):
    __tablename__ = "users"

    guid = Column(String, primary_key=True, index=True)
    activities = relationship(
        "ActivityModel", 
        secondary="user_activities", 
        back_populates="owners",
        lazy="selectin"
    )
    saved_activities = relationship(
        "ActivityModel", 
        secondary="user_saved_activities", 
        back_populates="saved_by_owners", 
        lazy="selectin"
    )


class ActivityModel(Base):
    __tablename__ = "activities"

    guid = Column(String, primary_key=True, index=True)

    category = Column(String)
    title = Column(String)
    desc = Column(String)
    date = Column(DateTime(timezone=True))
    location = Column(String)
    value = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    url = Column(String, nullable=True)

    owners = relationship(
        "UserModel",
        secondary="user_activities",
        back_populates="activities"
    )

    saved_by_owners = relationship(
        "UserModel", 
        secondary="user_saved_activities", 
        back_populates="saved_activities"
    )

    @property
    def coordinates(self):
        if self.url:
            return from_map_url_to_coordinates(self.url)
        return [0.0,0.0]


user_activities = Table(
    "user_activities",
    Base.metadata,
    Column("user_guid", String, ForeignKey("users.guid"), primary_key=True),
    Column("activity_guid", String, ForeignKey("activities.guid"), primary_key=True)
)

user_saved_activities = Table(
    "user_saved_activities",
    Base.metadata,
    Column("user_guid", String, ForeignKey("users.guid"), primary_key=True),
    Column("activity_guid", String, ForeignKey("activities.guid"), primary_key=True),
)