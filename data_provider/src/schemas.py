from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from src.enums import RPGStatus


class CreateEvent(BaseModel):
    """
    Represents a create event in the data provider.

    Attributes:
        hotel_id (int): The ID of the hotel associated with the event.
        timestamp (datetime): The timestamp of the event.
        rpg_status (RPGStatus): The RPG status of the event.
        room_id (int): The ID of the room associated with the event.
        night_of_stay (date): The date of the night of stay for the event.
    """

    hotel_id: int
    timestamp: datetime
    rpg_status: RPGStatus
    room_id: str
    night_of_stay: date


class ReadEvent(CreateEvent):
    """
    Represents a read event in the data provider. Inherits from CreateEvent.

    Attributes:
        id (int): The ID of the event.
        hotel_id (int): The ID of the hotel associated with the event.
        timestamp (datetime): The timestamp of the event.
        rpg_status (RPGStatus): The RPG status of the event.
        room_id (int): The ID of the room associated with the event.
        night_of_stay (date): The date of the night of stay for the event.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
