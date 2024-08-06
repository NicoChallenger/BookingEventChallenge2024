from sqlalchemy import extract
from sqlalchemy.orm import Session
from src import models, schemas, enums


def get_booking_events_for_year(
    db: Session,
    hotel_id: int,
    year: int,
) -> list[schemas.ReadEvent]:
    """
    Retrieve booking events for a specific hotel and year.

    Args:
        db (Session): The database session.
        hotel_id (int): The ID of the hotel.
        year (int): The year for which to retrieve booking events.

    Returns:
        list[schemas.ReadEvent]: A list of booking events for the specified hotel and year.
    """

    query = db.query(models.Event).filter(models.Event.hotel_id == hotel_id)
    query = query.filter(models.Event.rpg_status == enums.RPGStatus.BOOKING)
    query = query.filter(extract("year", models.Event.night_of_stay) == year)
    results = []
    for event in query.all():
        results.append(schemas.ReadEvent.model_validate(event))
    return results


def get_newest_booking(db: Session) -> schemas.ReadEvent | None:
    """
    Retrieve the newest booking from the database.

    Args:
        db (Session): The database session.

    Returns:
        schemas.ReadEvent | None: The newest booking as a ReadEvent object, or None if no booking is found.
    """
    query = db.query(models.Event).order_by(models.Event.timestamp.desc())
    event = query.first()
    if event:
        return schemas.ReadEvent.model_validate(event)
    return None


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
    db.commit()
    db.refresh(db_event)
    return db_event
