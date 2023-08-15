import pytest
from unittest import mock

from elevator import ForbiddenActionError, ElevatorStatus, Elevator

from tests.fixtures import elevator, passenger


def test_el_call_adds_floor_to_calls(passenger, elevator):
    spawn_floor = 2
    elevator._current_floor = 1
    passenger.spawn_floor = spawn_floor

    assert len(elevator._calls) == 0

    passenger.act_on_status(elevator)

    assert spawn_floor in elevator._calls
    assert len(elevator._calls) == 1


@mock.patch('elevator.Elevator.is_full')
def test_el_enter_not_allowed_if_is_full(is_full_mock: mock.Mock, passenger, elevator):
    is_full_mock.return_value = True
    elevator._doors_open = True

    with pytest.raises(ForbiddenActionError):
        elevator.enter(passenger)


@mock.patch('elevator.Elevator.is_full')
def test_el_enter_not_allowed_if_doors_closed(is_full_mock: mock.Mock, passenger, elevator):
    is_full_mock.return_value = False
    elevator._doors_open = False

    with pytest.raises(ForbiddenActionError):
        elevator.enter(passenger)


def test_el_created_in_correct_status(elevator):
    assert elevator._status == ElevatorStatus.IDLE


def test_el_changes_status_correctly_with_call_above(elevator: Elevator):
    elevator._calls.add(5)
    elevator._update_status()

    assert elevator._status == ElevatorStatus.MOVING_UP


def test_el_changes_status_correctly_with_call_bellow(elevator: Elevator):
    elevator._current_floor = 5
    elevator._calls.add(1)
    elevator._update_status()

    assert elevator._status == ElevatorStatus.MOVING_DOWN


def test_el_becomes_idle_when_no_calls(elevator: Elevator):
    elevator._status = ElevatorStatus.MOVING_UP
    elevator._calls = set()
    elevator._stops = set()

    elevator._update_status()

    assert elevator._status == ElevatorStatus.IDLE
