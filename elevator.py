from enum import Enum


class ForbiddenActionError(Exception):
    pass


class ElevatorStatus(Enum):
    IDLE = 1
    MOVING_UP = 2
    MOVING_DOWN = 3


class Elevator:

    def __init__(self, capacity: int, floors_number: int, initial_floor: int = 1):
        """
        :param capacity: possible number of people inside Elevator
        :param floors_number: number of existing floors
        :param initial_floor: floor to start from
        """
        self._current_floor: int = initial_floor
        self._floors_number: int = floors_number
        self._capacity: int = capacity
        self._doors_open: bool = False

        self._status: ElevatorStatus = ElevatorStatus.IDLE

        self._calls = set()
        self._stops = set()
        self._passengers = set()

    @property
    def is_full(self) -> bool:
        """
        Checks if capacity of Elevator is reached
        """
        return len(self._passengers) == self._capacity

    @property
    def current_floor(self) -> int:
        return self._current_floor

    @property
    def doors_open(self) -> bool:
        return self._doors_open

    def _open_doors(self) -> None:
        if not self._doors_open:
            print(f'Opening doors on {self.current_floor} floor')
        self._doors_open = True

    def _close_doors(self) -> None:
        if self._doors_open:
            print(f'Closing doors on {self.current_floor} floor')
        self._doors_open = False

    def _update_status(self) -> None:
        """
        Using simple algorithm by moving to first found target from stored stops or calls.

        But to slightly optimize passengers journey we changing direction only if there is no more stops or calls
        in the current moving direction.
        """
        stops_and_calls = self._calls.union(self._stops)

        if not stops_and_calls:
            self._status = ElevatorStatus.IDLE
            return

        # if there is any stop or call starts moving to the first one found
        if self._status == ElevatorStatus.IDLE and stops_and_calls:
            target_floor = list(stops_and_calls)[0]

            if target_floor > self.current_floor:
                self._status = ElevatorStatus.MOVING_UP
            elif target_floor < self.current_floor:
                self._status = ElevatorStatus.MOVING_DOWN

        elif self._status == ElevatorStatus.MOVING_UP:
            targets_higher = len([target for target in stops_and_calls if target > self.current_floor])

            if not targets_higher:
                self._status = ElevatorStatus.MOVING_DOWN

        elif self._status == ElevatorStatus.MOVING_DOWN:
            targets_lower = len([target for target in stops_and_calls if target < self.current_floor])

            if not targets_lower:
                self._status = ElevatorStatus.MOVING_UP

    def _move(self):
        if self._status == ElevatorStatus.MOVING_UP and self.current_floor != self._floors_number:
            self._current_floor += 1
            print(f'Moving up to {self.current_floor} floor')

        if self._status == ElevatorStatus.MOVING_DOWN and self.current_floor != 1:
            self._current_floor -= 1
            print(f'Moving down to {self.current_floor} floor')

    def move(self) -> None:
        """
        The main method to handle all of actions like
        closing/opening doors, updating status and moving from floor to floor.

        Elevator opens doors for every known stop to let passengers leave,
        for calls doors open only if Elevator is not full.
        """
        self._close_doors()

        self._update_status()
        self._move()

        if self.current_floor in self._stops:
            self._open_doors()
            self._stops.remove(self.current_floor)

        if self.current_floor in self._calls and not self.is_full:
            self._open_doors()
            self._calls.remove(self.current_floor)

    def call(self, floor: int) -> None:
        """
        Adds floor to where passenger have to be picked up
        """
        self._calls.add(floor)

    def enter(self, passenger: 'Passenger') -> None:
        """
        Lets passenger enter the Elevator if it's not full
        and add stop depending on its destination.
        """
        if self.is_full or not self.doors_open:
            raise ForbiddenActionError('Elevator is full or doors are closed')
        self._passengers.add(passenger)
        self._stops.add(passenger.destination)

    def leave(self, passenger: 'Passenger') -> None:
        """
        Lets passenger leave elevator on current floor
        """
        if not self.doors_open:
            raise ForbiddenActionError('Can\'t leave elevator while doors closed')
        self._passengers.remove(passenger)

    def print_current_state(self):
        state_string = (
            f'Elevator state:'
            f'\n\t Floor: {self.current_floor}'
            f'\n\t Passengers: {self._passengers}'
            f'\n\t Calls: {self._calls}'
            f'\n\t Stops: {self._stops}'
            f'\n\t Status: {self._status.name}'
            f'\n\t Doors: {"open" if self.doors_open else "closed"}'

        )
        print(state_string)


class PassengerStatus(Enum):
    """
    Statuses meaning:

    SPAWNED - Passenger just spawned on the floor, ready to call an Elevator;
    WAITING - Passenger called an Elevator and waiting its arrival;
    TRAVELING - Passenger is in Elevator on the way to destination floor;
    ON_DESTINATION - Passenger left an Elevator on the destination floor.
    """
    SPAWNED = 1
    WAITING = 2
    TRAVELING = 3
    ON_DESTINATION = 4


class Passenger:

    def __init__(self, spawn_floor: int, destination: int):
        self.spawn_floor: int = spawn_floor
        self.destination: int = destination

        self.status = PassengerStatus.SPAWNED

    def act_on_status(self, elevator: Elevator):
        """
        Performs Passenger actions depending on Passenger's current status
        and Elevator's current floor

        Possible status transitions:
        ----------------------------
        SPAWNED: WAITING;
        WAITING: SPAWNED, TRAVELING;
        TRAVELING: ON_DESTINATION;
        ON_DESTINATION: -
        """
        # call the elevator when spawned
        if self.status == PassengerStatus.SPAWNED:
            elevator.call(self.spawn_floor)
            self.status = PassengerStatus.WAITING

        # try to enter the elevator on spawn floor
        if self.status == PassengerStatus.WAITING:
            if elevator.current_floor == self.spawn_floor and elevator.doors_open:
                try:
                    elevator.enter(self)
                except ForbiddenActionError:
                    self.status = PassengerStatus.SPAWNED
                else:
                    self.status = PassengerStatus.TRAVELING

        # try to leave the elevator on destination floor
        if self.status == PassengerStatus.TRAVELING:
            if elevator.current_floor == self.destination and elevator.doors_open:
                try:
                    elevator.leave(self)
                except ForbiddenActionError:
                    pass
                else:
                    self.status = PassengerStatus.ON_DESTINATION

    def __repr__(self):
        return (f'Passenger. Id: {id(self)}, Status: {self.status.name}, '
                f'Spawn floor: {self.spawn_floor}, Dest: {self.destination}')
