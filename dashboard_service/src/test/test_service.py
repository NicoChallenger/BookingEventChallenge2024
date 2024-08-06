from datetime import date, datetime
from src import schemas
from src.enums import RPGStatus
from src.service import group_events_by_day, group_events_by_month


def test_group_events_by_month():
    """
    Test function for grouping events by month.

    This function creates sample events and calls the `group_events_by_month` function
    to group the events by month. It then asserts that the result matches the expected
    output.

    Returns:
        None
    """
    # Create sample events
    events = [
        schemas.ReadEvent(
            id=0,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 1, 5),
        ),
        schemas.ReadEvent(
            id=1,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 1, 10),
        ),
        schemas.ReadEvent(
            id=2,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 2, 15),
        ),
        schemas.ReadEvent(
            id=3,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 3, 20),
        ),
        schemas.ReadEvent(
            id=4,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 3, 25),
        ),
        schemas.ReadEvent(
            id=5,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 4, 1),
        ),
    ]

    # Call the function
    result = group_events_by_month(events, 2022)
    # Assert the result
    assert result == {
        date(2022, 1, 1).isoformat(): 2,
        date(2022, 2, 1).isoformat(): 1,
        date(2022, 3, 1).isoformat(): 2,
        date(2022, 4, 1).isoformat(): 1,
        date(2022, 5, 1).isoformat(): 0,
        date(2022, 6, 1).isoformat(): 0,
        date(2022, 7, 1).isoformat(): 0,
        date(2022, 8, 1).isoformat(): 0,
        date(2022, 9, 1).isoformat(): 0,
        date(2022, 10, 1).isoformat(): 0,
        date(2022, 11, 1).isoformat(): 0,
        date(2022, 12, 1).isoformat(): 0,
    }


def test_group_events_by_day():
    """
    Test function for grouping events by day.

    This function creates sample events and calls the `group_events_by_day` function
    to group the events by day. It then asserts that the result matches the expected
    output.

    Returns:
        None
    """
    # Create sample events
    events = [
        schemas.ReadEvent(
            id=0,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 1, 5),
        ),
        schemas.ReadEvent(
            id=1,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 1, 10),
        ),
        schemas.ReadEvent(
            id=2,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 2, 15),
        ),
        schemas.ReadEvent(
            id=3,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 3, 20),
        ),
        schemas.ReadEvent(
            id=4,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 3, 25),
        ),
        schemas.ReadEvent(
            id=5,
            hotel_id=0,
            timestamp=datetime.now(),
            rpg_status=RPGStatus.BOOKING,
            room_id="0",
            night_of_stay=date(2022, 4, 1),
        ),
    ]
    # Call the function
    result = group_events_by_day(events, 2022)

    # Assert the result
    assert result[date(2022, 1, 5).isoformat()] == 1
    assert result[date(2022, 1, 10).isoformat()] == 1
    assert result[date(2022, 2, 15).isoformat()] == 1
    assert result[date(2022, 3, 20).isoformat()] == 1
    assert result[date(2022, 3, 25).isoformat()] == 1
    assert result[date(2022, 4, 1).isoformat()] == 1
