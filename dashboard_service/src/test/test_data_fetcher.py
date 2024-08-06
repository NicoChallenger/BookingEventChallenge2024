from datetime import date, datetime
from unittest.mock import Mock, patch
from src import config, schemas
from src.data_fetcher import fetch_events
from src.enums import RPGStatus


@patch("src.data_fetcher.requests.get")
def test_fetch_events(mock_get: Mock):
    """
    Test case for the fetch_events function. Mocks the requests.get method to return a list of events.
    """

    # Mock the response from the requests.get method
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = [
        {
            "id": 1,
            "hotel_id": 0,
            "rpg_status": 1,
            "room_id": "0",
            "night_of_stay": date(2022, 1, 6).isoformat(),
            "timestamp": datetime(2022, 1, 1).isoformat(),
        },
        {
            "id": 2,
            "hotel_id": 0,
            "rpg_status": 1,
            "room_id": "1",
            "night_of_stay": date(2022, 1, 7).isoformat(),
            "timestamp": datetime(2022, 1, 1).isoformat(),
        },
    ]
    mock_get.return_value = mock_response

    # Define the expected start and end timestamps
    start_timestamp = datetime(2022, 1, 1)
    end_timestamp = datetime(2022, 1, 2)

    # Call the fetch_events function
    events = fetch_events(start_timestamp, end_timestamp)

    # Assert the requests.get method was called with the correct parameters
    mock_get.assert_called_once_with(
        f"{config.DATA_PROVIDER_URL}/events",
        params={
            "updated__gte": "2022-01-01T00:00:00",
            "updated__lte": "2022-01-02T00:00:00",
        },
        timeout=5,    
    )

    # Assert the returned events match the expected events
    expected_events = [
        schemas.ReadEvent(
            id=1,
            hotel_id=0,
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 1, 6),
            timestamp=datetime(2022, 1, 1),
        ),
        schemas.ReadEvent(
            id=2,
            hotel_id=0,
            rpg_status=RPGStatus.BOOKING,
            room_id="1",
            night_of_stay=date(2022, 1, 7),
            timestamp=datetime(2022, 1, 1),
        ),
    ]
    assert events == expected_events
