import pytest
from unittest import mock

from elevator import PassengerStatus, Passenger

from tests.fixtures import elevator, passenger


def test_pas_created_with_correct_status():
    p = Passenger(1, 10)
    assert p.status == PassengerStatus.SPAWNED


@mock.patch('elevator.Elevator.call')
def test_pas_calls_el_when_spawned(call_mock: mock.Mock, passenger, elevator):
    assert passenger.status == PassengerStatus.SPAWNED
    passenger.act_on_status(elevator)
    call_mock.assert_called_once_with(passenger.spawn_floor)


def test_pas_changes_status_when_el_called(passenger, elevator):
    assert passenger.status == PassengerStatus.SPAWNED

    # set floor different from elevator's floor, so passenger has to wait
    passenger.spawn_floor = 2

    passenger.act_on_status(elevator)
    assert passenger.status == PassengerStatus.WAITING


@pytest.mark.parametrize("passenger", [PassengerStatus.WAITING], indirect=True)
@mock.patch('elevator.Elevator.enter')
def test_waiting_pas_tries_enter_el_on_same_floor(enter_mock: mock.Mock, passenger, elevator):
    elevator._current_floor = passenger.spawn_floor
    elevator._doors_open = True

    passenger.act_on_status(elevator)

    enter_mock.assert_called_once_with(passenger)
    assert passenger.status == PassengerStatus.TRAVELING


@pytest.mark.parametrize("passenger", [PassengerStatus.WAITING], indirect=True)
@mock.patch('elevator.Elevator.is_full')
def test_waiting_pas_become_spawned_after_waiting(
        is_full_mock: mock.Mock,
        passenger,
        elevator
):
    """
    Passenger should change status on SPAWNED if he tried to enter to full Elevator
    """
    is_full_mock.return_value = True
    elevator._current_floor = passenger.spawn_floor
    elevator._doors_open = True

    passenger.act_on_status(elevator)

    assert passenger.status == PassengerStatus.SPAWNED

