# Elevator simulation

## Description
Simulation of elevator serving passengers which randomly spawning on floors,
calling elevator and going to their destinations.

`elevator.py` - source code of Passenger and Elevator classes

`simulator.py` - entrypoint of simulation


## Setup and run

- Use python@3.10 or above
- Clone repository
- Create virtual env
- Run following:
  - `pip install -r requirements.txt`
  - `python simulator.py`

TIP: adjust creation of `Simulator` instance in `simulator.py` to get desired simulation results.

### Tests
- `pytest --cov=elevator`
