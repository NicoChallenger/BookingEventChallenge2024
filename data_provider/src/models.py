from sqlalchemy import  Column, Date, DateTime, Enum, Integer, String

from src.enums import RPGStatus
from .database import Base


class Event(Base):
    """
    Represents an event in the system.

    Attributes:
        id (int): The unique identifier of the event.
        hotel_id (int): The ID of the hotel associated with the event.
        timestamp (datetime): The timestamp of the event.
        rpg_status (int): The RPG status of the event.
        room_id (int): The ID of the room associated with the event.
        night_of_stay (date): The date of the night of stay for the event.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, index=True)
    timestamp = Column(DateTime(timezone=True))
    rpg_status = Column(Enum(RPGStatus))
    room_id = Column(String, unique=True)
    night_of_stay = Column(Date)
