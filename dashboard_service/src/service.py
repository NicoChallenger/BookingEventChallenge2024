from typing import List
from src import schemas
from datetime import date, timedelta


def group_events_by_month(events: List[schemas.ReadEvent], year: int) -> dict[str, int]:
    """
    Groups the events by month and returns a dictionary with the number of events for each month.

    Args:
        events (List[schemas.ReadEvent]): A list of events.
        year (int): The year for which to group the events.

    Returns:
        dict[date, int]: A dictionary where the keys are dates representing the start of each month
        and the values are the number of events for that month.
    """

    result_months = {}
    for month in range(1, 13):
        current_date = date(year, month, 1)
        # Filter events for the current month
        month_events = [event for event in events if event.night_of_stay.month == month]
        # Store the number of events for the current month
        result_months[current_date.isoformat()] = len(month_events)

    return result_months


def group_events_by_day(events: List[schemas.ReadEvent], year: int) -> dict[str, int]:
    """
    Groups events by day for a given year.

    Args:
        events (List[schemas.ReadEvent]): A list of events.
        year (int): The year for which to group the events.

    Returns:
        dict[date, int]: A dictionary where the keys are dates and the values are the number of events on that day.
    """
    result_days = {}
    end_date = date(year, 12, 31)
    start_date = date(year, 1, 1)
    # Calculate the number of days between the start and end date
    days = (end_date - start_date).days + 1

    for day in range(1, days + 1):
        # Filter events for the current day
        day_events = [event for event in events if event.night_of_stay == start_date]
        # Store the number of events for the current day
        result_days[start_date.isoformat()] = len(day_events)
        # Move to the next day
        start_date += timedelta(days=1)
    return result_days
