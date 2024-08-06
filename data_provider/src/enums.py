from enum import IntEnum


class RPGStatus(IntEnum):
    """
    Enum representing the status of an event wether it is a booking or a cancellation.

    Attributes:
        BOOKING (int): Represents the booking status.
        CANCELLATION (int): Represents the cancellation status.
    """

    BOOKING = 1
    CANCELLATION = 2