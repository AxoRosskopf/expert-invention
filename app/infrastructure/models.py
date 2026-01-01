import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Integer, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.utils import from_map_url_to_coordinates

class InteractionType(str, enum.Enum):
    VIEW = "view"
    IGNORE = "ignore"
    CLICK = "click"
    SAVE = "save"


class UserInteractionModel(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_guid = Column(String, ForeignKey("users.guid"), index=True)
    activity_guid = Column(String, ForeignKey("activities.guid"), index=True)

    action = Column(SqlEnum(InteractionType))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="interactions")
    activity = relationship("ActivityModel")

class UserModel(Base):
    __tablename__ = "users"

    guid = Column(String, primary_key=True, index=True)

    saved_activities = relationship(
        "ActivityModel", 
        secondary="user_saved_activities", 
        back_populates="saved_by_owners", 
        lazy="selectin"
    )

    interactions = relationship(
        "UserInteractionModel",
        back_populates="user",
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


user_saved_activities = Table(
    "user_saved_activities",
    Base.metadata,
    Column("user_guid", String, ForeignKey("users.guid"), primary_key=True),
    Column("activity_guid", String, ForeignKey("activities.guid"), primary_key=True),
)