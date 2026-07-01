"""nature_basic_simulation.py

This module runs the nature simulation using the given entities"""
import random
import time

from alerts import PredatorEatHerbivoreAlert, DeadEntityAlert, ManyPlantsAlert, EventManager
from entities import Herbivore, Plant, Predator, Rock, Ground
from entities.entity import Entity
from entities.mobile_entity import MobileEntity

ENTITY_MAP = {
    cls.SIGN: cls
    for cls in [Plant, Herbivore, Predator, Rock, Ground]
}

def init_board():
    board = []

    with open("nature_board.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            board_row = []

            for col, symbol in enumerate(line.strip()):
                entity_class = ENTITY_MAP.get(symbol)

                if entity_class:
                    board_row.append(entity_class(row, col))

            board.append(board_row)

    return board


def print_board(board: list):
    """Prints the board."""
    for row in board:
        for cell in row:
            cell.print_entity()
        print()
    print()


def spawn_random_plant(board : list):
    """Plants appear randomly at empty spaces."""

    empty_cells = []
    for row_idx, row in enumerate(board):
        for col_idx, col in enumerate(row):
            if isinstance(col, Ground):
                empty_cells.append((row_idx, col_idx))
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = Plant(r, c)

def get_all_subclasses(base_class):
    """Return all subclasses without recursion."""
    subclasses = []
    queue = list(base_class.__subclasses__())

    while queue:
        current = queue.pop(0)
        subclasses.append(current)
        queue.extend(current.__subclasses__())

    return subclasses

def check_entity_extinction(board: list, events, entity_types: list):
    """Check if the given entities are on the board.xg"""
    seen_extinct: list = []
    for entity_type in entity_types:
        if entity_type.__name__ in seen_extinct:
            continue
        found = False
        for row in board:
            for cell in row:
                if isinstance(cell, entity_type):
                    found = True
        if not found:
            seen_extinct.append(entity_type.__name__)
            events.notify("ENTITY_EXTINCT", {"entity": entity_type.__name__})

def check_plant_overflow(board: list, events):
    plant_count = 0
    total_cells = 0

    for row in board:
        for cell in row:
            total_cells += 1
            if isinstance(cell, Plant):
                plant_count += 1

    if total_cells > 0 and (plant_count / total_cells) > 0.9:
        events.notify("PLANT_OVERFLOW")

def move_entities(board: list, events):
    """Moves the entities on the board according to each of the entities rules."""
    num_steps = 10

    for step in range(num_steps):
        print_board(board)
        entities_to_process = []

        for row_idx, row in enumerate(board):
            for col_idx, col in enumerate(row):
                cell = col
                if isinstance(cell, MobileEntity):
                    entities_to_process.append(cell)

        for entity in entities_to_process:
             entity.step(board, events)

        spawn_random_plant(board)
        check_entity_extinction(board, events, get_all_subclasses(Entity))
        check_plant_overflow(board, events)
        time.sleep(0.5)
    print_board(board)

def subscribe_events():
    events = EventManager()

    events.subscribe(
        "ENTITY_EXTINCT",
        DeadEntityAlert()
    )

    events.subscribe(
        "HERBIVORE_EATEN",
        PredatorEatHerbivoreAlert()
    )

    events.subscribe(
        "PLANT_OVERFLOW",
        ManyPlantsAlert()
    )

    return events

def main():
    """Run the program"""
    events = subscribe_events()
    board = init_board()
    move_entities(board, events)


if __name__ == "__main__":
    main()
