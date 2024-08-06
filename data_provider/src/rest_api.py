from datetime import date, datetime
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get(
    "/events",
    response_model=list[schemas.ReadEvent],
    summary="Retrieve events based on the provided filters",
)
def read_events(
    hotel_id: int | None = None,
    updated__gte: datetime | None = None,
    updated__lte: datetime | None = None,
    rpg_status: schemas.RPGStatus | None = None,
    room_id: str | None = None,
    night_of_stay__gte: date | None = None,
    night_of_stay__lte: date | None = None,
    db: Session = Depends(get_db),  # dependency injection
):
    """
    Retrieve events based on the provided filters.

    Args:
        hotel_id (int): The ID of the hotel.
        updated__gte (datetime | None, optional): The minimum updated datetime. Defaults to None.
        updated__lte (datetime | None, optional): The maximum updated datetime. Defaults to None.
        rpg_status (schemas.RPGStatus | None, optional): The RPG status. Defaults to None.
        room_id (int | None, optional): The ID of the room. Defaults to None.
        night_of_stay__gte (date | None, optional): The minimum night of stay date. Defaults to None.
        night_of_stay__lte (date | None, optional): The maximum night of stay date. Defaults to None.

    Returns:
        List[schemas.Event]: The list of events matching the provided filters.
    """

    events = crud.get_events(
        db,
        hotel_id=hotel_id,
        updated__gte=updated__gte,
        updated__lte=updated__lte,
        rpg_status=rpg_status,
        room_id=room_id,
        night_of_stay__gte=night_of_stay__gte,
        night_of_stay__lte=night_of_stay__lte,
    )

    return events


@app.post(
    "/events",
    response_model=schemas.CreateEvent,
    status_code=201,
    summary="Create a new event or cancle a booking",
)
def create_event(event: schemas.CreateEvent, db: Session = Depends(get_db)):
    """
    Create a new event. If the event is a cancellation, it will cancel the booking if it exists.
    This action is idempotent, meaning that a booking can be cancelled multiple times without any side effects.

    Args:
        event (schemas.CreateEvent): The event data to be created.

    Returns:
        schemas.CreateEvent: The created event data.

    """
    # Check if the event is a cancellation
    if event.rpg_status == schemas.RPGStatus.CANCELLATION:
        matched_events = crud.get_events(
            db,
            hotel_id=event.hotel_id,
            room_id=event.room_id,
        )
        if len(matched_events) > 0:
            # room_id is unique, so there is only one matched event
            if matched_events[0].rpg_status == schemas.RPGStatus.BOOKING:
                # Cancel the booking
                return crud.cancel_event(db=db, event_id=matched_events[0].id)
        else:
            raise HTTPException(
                status_code=404,
                detail="Booking not found, can't cancel unknown booking",
            )
    try:
        result = crud.create_event(db=db, event=event)
        return result
    except crud.DuplicateError:
        raise HTTPException(
            status_code=409,
            detail="Conflict: duplicate error, this event already exists.",
        )
