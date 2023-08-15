from typing import Optional

import pytest

from elevator import PassengerStatus, Passenger, Elevator


@pytest.fixture
def passenger(status: Optional[PassengerStatus] = None) -> Passenger:
    passenger = Passenger(1, 10)

    if status is not None:
        passenger.status = status

    return passenger


@pytest.fixture
def elevator() -> Elevator:
    return Elevator(1, 10)
