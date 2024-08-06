import asyncio
from datetime import datetime, timedelta
import requests
from sqlalchemy.orm import Session
from src import config, schemas, crud
from src.database import get_db


def fetch_events(
    start_timestamp: datetime, end_timestamp: datetime
) -> list[schemas.ReadEvent]:
    """
    Fetches events from the data provider API within the specified time range.

    Args:
        start_timestamp (datetime): The start timestamp of the time range.
        end_timestamp (datetime): The end timestamp of the time range.

    Returns:
        list[schemas.ReadEvent]: A list of ReadEvent objects representing the fetched events.
    """
    print(f"Fetching events from {start_timestamp} to {end_timestamp}")

    response = requests.get(
        f"{config.DATA_PROVIDER_URL}/events",
        params={
            "updated__gte": start_timestamp.isoformat(),
            "updated__lte": end_timestamp.isoformat(),
        },
        timeout=5,
    )

    if not response.ok:
        print(f"Failed to fetch events: {response.text}")
        response.raise_for_status()
    event_list = response.json()

    return [schemas.ReadEvent(**event) for event in event_list]


def update_data(db: Session, start_timestamp: datetime) -> datetime:
    """
    Update data in the database from a given start timestamp.

    Args:
        db (Session): The database session.
        start_timestamp (datetime): The start timestamp to fetch events from.

    Returns:
        datetime: The end timestamp of the data update.

    """
    end_timestamp = datetime.now()
    events = fetch_events(start_timestamp, end_timestamp)
    for event in events:
        # remove internal id from data provider
        event.id = None
        # TODO: make this batch processable
        crud.create_event(db=db, event=event)
    return end_timestamp


async def extraction_loop() -> None:
    """
    Asynchronous function that continuously extracts data from the data_provider.

    This function retrieves the latest event timestamp from the database and starts extracting data from that point onwards.
    If there are no events in the database, it starts from the beginning of the current year.
    The function then enters an infinite loop where it continuously updates the data by calling the `update_data` function.
    If an exception occurs during the data update, an error message is printed.
    The function waits for 5 seconds between each data update.

    """
    db = next(get_db())
    print("Starting data extraction loop ...")
    # Get the latest event timestamp
    latest_event = crud.get_newest_booking(db=db)
    # If there are no events, start from the beginning of the year
    epoch_year = datetime.today().year
    latest_timestamp = datetime(epoch_year, 1, 1)
    # If there are events, start from the latest event timestamp + 1 second
    if latest_event:
        latest_timestamp = latest_event.timestamp + timedelta(seconds=1)

    while True:
        try:
            latest_timestamp = update_data(db=db, start_timestamp=latest_timestamp)
        except requests.RequestException as e:
            print(f"Failed to update event data: {e}")
        await asyncio.sleep(5)
