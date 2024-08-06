from fastapi.testclient import TestClient
from datetime import datetime, date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src import models
from src.enums import RPGStatus


def test_get_dashboard(rest_client: TestClient, mock_db: Session) -> None:
    """
    Test case for the get_dashboard endpoint.

    This function tests the get_dashboard endpoint by creating test data, making a request to the endpoint,
    and asserting the response based on the period (MONTH or DAY).

    Args:
        rest_client (TestClient): The test client fixture for making HTTP requests.
        mock_db (Session): The mocked database session fixture.
    """

    # Create test data for bookings in a year
    event1 = models.Event(
        id=1,
        hotel_id=1,
        timestamp=datetime(2024, 1, 15),  # January
        rpg_status=RPGStatus.BOOKING,
        room_id="0",
        night_of_stay=date(2024, 1, 15),
    )
    event2 = models.Event(
        id=2,
        hotel_id=1,
        timestamp=datetime(2024, 1, 20),  # January
        rpg_status=RPGStatus.BOOKING,
        room_id="1",
        night_of_stay=date(2024, 1, 20),
    )
    event3 = models.Event(
        id=3,
        hotel_id=1,
        timestamp=datetime(2024, 2, 10),  # February
        rpg_status=RPGStatus.BOOKING,
        room_id="2",
        night_of_stay=date(2024, 2, 10),
    )
    mock_db.add(event1)
    mock_db.add(event2)
    mock_db.add(event3)
    mock_db.commit()

    # Test for MONTH period
    response_month = rest_client.get(
        "/dashboard",
        params={
            "hotel_id": 1,
            "period": "month",
            "year": 2024,
        },
    )
    # Assert the response for MONTH period
    assert response_month.status_code == 200  # TODO: 404  not found currently!!!
    data_month = response_month.json()
    assert len(data_month) == 12  # 12 months in a year
    assert data_month["2024-01-01"] == 2  # Two events in January
    assert data_month["2024-02-01"] == 1  # One event in February

    # Test for DAY period
    response_day = rest_client.get(
        "/dashboard",
        params={
            "hotel_id": 1,
            "period": "day",
            "year": 2024,
        },
    )

    # Assert the response for DAY period
    assert response_day.status_code == 200
    data_day = response_day.json()
    assert len(data_day) == 366  # Leap year
    assert data_day["2024-01-15"] == 1  # One event on 2024-01-15
    assert data_day["2024-01-20"] == 1  # One event on 2024-01-20
    assert data_day["2024-02-10"] == 1  # One event on 2024-02-10
