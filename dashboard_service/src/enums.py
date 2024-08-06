from enum import Enum, IntEnum


class RPGStatus(IntEnum):
    """
    Enum representing the status of an event wether it is a booking or a cancellation.

    Attributes:
        BOOKING (int): Represents the booking status.
        CANCELLATION (int): Represents the cancellation status.
    """

    BOOKING = 1
    CANCELLATION = 2


class DashboardPeriod(str, Enum):
    """
    Enum representing the period of the dashboard.

    Attributes:
        MONTH (str): Represents the month period.
        DAY (str): Represents the day period.
    """

    MONTH = "month"
    DAY = "day"
    