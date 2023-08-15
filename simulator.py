import random

from elevator import Elevator, Passenger, PassengerStatus


class Simulator:

    def __init__(self,
                 max_passengers: int,
                 total_passengers_to_serve: int,
                 spawn_probability: int,
                 floors_num: int,
                 elevator_capacity: int):
        """

        :param max_passengers: How much passengers may be in the simulation at one moment
        :param total_passengers_to_serve: How much passengers we want to serve in total
        :param spawn_probability: The chance that passenger will be spawned on each turn
        :param floors_num: How much floors elevator has to serve
        :param elevator_capacity: How much passengers can hold an elevator
        """
        assert floors_num > 1, 'You have to set more than 1 floor'

        self.FLOORS_NUM = floors_num
        self.MAX_PASSENGERS = max_passengers
        self.SPAWN_PROBABILITY = spawn_probability
        self.TOTAL_PASSENGERS = total_passengers_to_serve

        self.total_passengers_spawned = 0

        self._passengers = {}  # using dict instead of set to serve passengers in the order they spawned

        self.elevator = Elevator(capacity=elevator_capacity, floors_number=floors_num)

    @property
    def passengers(self) -> list[Passenger]:
        return list(self._passengers.keys())

    def add_passenger(self, p: Passenger) -> None:
        print(f'(+) New passenger: {p}')
        self._passengers[p] = None
        self.total_passengers_spawned += 1

    def remove_passenger(self, p: Passenger) -> None:
        print(f'(!) Passenger reached destination: {p}')
        del self._passengers[p]

    @property
    def max_passengers_reached(self) -> bool:
        """
        :return: True if number of serving passengers at the moment is reached self.MAX_PASSENGERS
        """
        return len(self.passengers) == self.MAX_PASSENGERS

    @property
    def total_passengers_reached(self) -> bool:
        """
        :return: True if total number of spawned passengers during simulation is reached self.TOTAL_PASSENGERS
        """
        return self.total_passengers_spawned == self.TOTAL_PASSENGERS

    def check_spawn_chance(self) -> bool:
        """
        :return: True if chance of spawning was hit
        """
        return random.randint(1, 101) <= self.SPAWN_PROBABILITY

    def spawn_passenger(self) -> None:
        """
        Spawns new passenger with change depending on self.SPAWN_PROBABILITY
        """
        if (
                self.check_spawn_chance()
                and not self.max_passengers_reached
                and not self.total_passengers_reached
        ):
            spawn_floor = random.randint(1, self.FLOORS_NUM)
            # assume passenger not going to move to the same floor he was spawned
            # so exclude spawn_floor from possible choices
            destination = random.choice([i for i in range(1, self.FLOORS_NUM + 1) if i != spawn_floor])

            p = Passenger(spawn_floor, destination)
            self.add_passenger(p)

    def print_passengers_state(self):
        if self.passengers:
            print('Passengers:')
        for p in self.passengers:
            print(f'\t {p}')

    def perform_passengers_actions(self) -> None:
        """
        Makes each passenger act, removes passengers reached their destination
        """
        for p in self.passengers:
            p.act_on_status(self.elevator)
            if p.status == PassengerStatus.ON_DESTINATION:
                self.remove_passenger(p)

    def run(self):
        """
        The entrypoint of simulation.
        Runs a loop until we spawn self.TOTAL_PASSENGERS and serve each of them to their destinations.
        """
        print('=' * 100)
        self.elevator.print_current_state()

        while self.passengers or not self.total_passengers_reached:
            print('=' * 100)
            self.spawn_passenger()
            self.perform_passengers_actions()
            print('-' * 10)
            self.elevator.move()
            self.elevator.print_current_state()
            print('-' * 10)
            self.print_passengers_state()

        print(f'Passengers served: {self.total_passengers_spawned}')


s = Simulator(
    max_passengers=2,
    spawn_probability=50,
    floors_num=10,
    total_passengers_to_serve=15,
    elevator_capacity=5
)

s.run()
