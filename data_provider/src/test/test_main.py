from datetime import datetime, date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src import models, schemas


def test_read_events(rest_client: TestClient, mock_db: Session) -> None:
    """
    Test case for the read_events endpoint.

    This function tests the read_events endpoint by creating test data, making a request to the endpoint,
    and asserting the response.

    Args:
        rest_client (TestClient): The test client fixture for making HTTP requests.
        mock_db (Session): The mocked database session fixture.

    """

    # Create test data
    event = models.Event(
        id=1,
        hotel_id=1,
        timestamp=datetime(2024, 9, 9),
        rpg_status=1,
        room_id="0",
        night_of_stay=date(2022, 10, 10),
    )
    mock_db.add(event)
    event = models.Event(
        id=2,
        hotel_id=42,
        timestamp=datetime(2024, 11, 11),
        rpg_status=2,
        room_id="3",
        night_of_stay=date(2024, 12, 12),
    )
    mock_db.add(event)
    mock_db.commit()

    # Execute endpoint request
    response = rest_client.get(
        "/events",
        params={
            "hotel_id": 1,
            "updated__gte": datetime(2022, 1, 1),
            "updated__lte": datetime(2025, 1, 31),
            "rpg_status": schemas.RPGStatus.BOOKING.value,
            "room_id": "0",
            "night_of_stay__gte": date(2022, 1, 1),
            "night_of_stay__lte": date(2025, 1, 31),
        },
    )

    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["hotel_id"] == 1
    assert datetime.fromisoformat(data[0]["timestamp"]) >= datetime(2022, 1, 1)
    assert datetime.fromisoformat(data[0]["timestamp"]) <= datetime(2025, 1, 31)
    assert data[0]["rpg_status"] == schemas.RPGStatus.BOOKING.value
    assert data[0]["room_id"] == "0"
    assert date.fromisoformat(data[0]["night_of_stay"]) >= date(2022, 1, 1)
    assert date.fromisoformat(data[0]["night_of_stay"]) <= date(2025, 1, 31)


def test_read_no_event(rest_client: TestClient) -> None:
    """
    Test case for reading events when no events are available.

    Args:
        rest_client (TestClient): The test client fixture for making HTTP requests.
    """

    # Execute endpoint request
    response = rest_client.get(
        "/events",
        params={
            "hotel_id": 1,
        },
    )

    # Assert the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_create_event(rest_client: TestClient, mock_db: Session) -> None:
    """
    Test case for creating an event.

    Args:
        rest_client (TestClient): The test client fixture for making HTTP requests.
        mock_db (Session): The mock database session fixture.
    """

    # Create test data
    event = schemas.CreateEvent(
        hotel_id=1,
        timestamp=datetime(2022, 1, 1),
        rpg_status=schemas.RPGStatus.BOOKING,
        room_id="2",
        night_of_stay=date(2022, 1, 1),
    )

    # Test the endpoint
    response = rest_client.post("/events", json=event.model_dump(mode="json"))

    # Assert the response
    assert response.status_code == 201

    # Assert values in the database
    db_data = mock_db.query(models.Event).filter(models.Event.hotel_id == 1).all()
    assert len(db_data) == 1
    assert db_data[0].hotel_id == 1
    assert db_data[0].timestamp == datetime(2022, 1, 1)
    assert db_data[0].rpg_status == schemas.RPGStatus.BOOKING
    assert db_data[0].room_id == "2"
    assert db_data[0].night_of_stay == date(2022, 1, 1)


def test_cancel_event(rest_client: TestClient, mock_db: Session) -> None:
    """
    Test case for cancelling an event.

    Args:
        rest_client (TestClient): The test client fixture for making HTTP requests.
        mock_db (Session): The mock database session fixture.
    """

    # Create a booking event in the database
    event = models.Event(
        id=1,
        hotel_id=1,
        timestamp=datetime(2024, 1, 1),
        rpg_status=1,
        room_id="0",
        night_of_stay=date(2024, 2, 2),
    )
    # Insert the booking event into the mock database
    mock_db.add(event)
    mock_db.commit()

    # Create a cancellation event
    cancellation_event = schemas.CreateEvent(
        hotel_id=1,
        timestamp=datetime(2022, 1, 2),  # Different timestamp
        rpg_status=schemas.RPGStatus.CANCELLATION,
        room_id="0",
        night_of_stay=date(2022, 1, 1),
    )

    # Test the endpoint for cancellation
    response = rest_client.post(
        "/events", json=cancellation_event.model_dump(mode="json")
    )

    # Assert the response
    assert response.status_code == 201

    # Assert values in the database
    db_data = mock_db.query(models.Event).filter(models.Event.hotel_id == 1).all()
    assert len(db_data) == 1  # Only one event should exist due to cancellation
    assert db_data[0].hotel_id == 1
    assert db_data[0].timestamp == datetime(
        2024, 1, 1
    )  # The timestamp of the cancellation event
    assert db_data[0].rpg_status == schemas.RPGStatus.CANCELLATION
    assert db_data[0].room_id == "0"
    assert db_data[0].night_of_stay == date(2024, 2, 2)
