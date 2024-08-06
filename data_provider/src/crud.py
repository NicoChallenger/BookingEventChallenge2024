from datetime import datetime, date
import sqlite3
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm import Session
from . import models, schemas


class DuplicateError(Exception):
    pass


def get_events(
    db: Session,
    hotel_id: int | None = None,
    updated__gte: datetime | None = None,
    updated__lte: datetime | None = None,
    rpg_status: schemas.RPGStatus | None = None,
    room_id: int | None = None,
    night_of_stay__gte: date | None = None,
    night_of_stay__lte: date | None = None,
) -> list[models.Event]:
    """
    Retrieve events from the database based on the provided filters and return them sorted by timestamp in ascending order.
    The function works by compositing a query based on the provided filters and then executing it.
    Each filter is added to the query if it is not None and the query is then executed to retrieve the events.

    Args:
        db (Session): The database session.
        hotel_id (int): The ID of the hotel to filter events by.
        updated__gte (datetime | None, optional): The minimum timestamp for events to include. Defaults to None.
        updated__lte (datetime | None, optional): The maximum timestamp for events to include. Defaults to None.
        rpg_status (schemas.RPGStatus | None, optional): The RPG status to filter events by. Defaults to None.
        room_id (int | None, optional): The ID of the room to filter events by. Defaults to None.
        night_of_stay__gte (date | None, optional): The minimum night of stay for events to include. Defaults to None.
        night_of_stay__lte (date | None, optional): The maximum night of stay for events to include. Defaults to None.

    Returns:
        List[models.Event]: A list of events matching the provided filters.
    """
    query = db.query(models.Event)
    if hotel_id:
        query = query.filter(models.Event.hotel_id == hotel_id)

    if updated__gte:
        query = query.filter(models.Event.timestamp >= updated__gte)

    if updated__lte:
        query = query.filter(models.Event.timestamp <= updated__lte)

    if rpg_status:
        query = query.filter(models.Event.rpg_status == rpg_status)

    if room_id:
        query = query.filter(models.Event.room_id == room_id)

    if night_of_stay__gte:
        query = query.filter(models.Event.night_of_stay >= night_of_stay__gte)

    if night_of_stay__lte:
        query = query.filter(models.Event.night_of_stay <= night_of_stay__lte)

    return query.order_by(models.Event.timestamp.asc()).all()


def create_event(db: Session, event: schemas.CreateEvent) -> models.Event:
    """
    Create a new event in the database.

    Parameters:
    - db (Session): The database session.
    - event (CreateEvent): The event data to be created.

    Returns:
    - Event: The created event object.
    """
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print(f"Error creating event: {e}")
        db.rollback()
        raise DuplicateError("Duplicate data")
    db.refresh(db_event)
    return db_event


def cancel_event(db: Session, event_id: int) -> models.Event:
    """
    Cancel an event in the database.

    Parameters:
    - db (Session): The database session.
    - event_id (int): The ID of the event to be cancelled.

    Returns:
    - Event: The cancelled event object.
    """
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_event.rpg_status = schemas.RPGStatus.CANCELLATION
    db.commit()
    db.refresh(db_event)
    return db_event
