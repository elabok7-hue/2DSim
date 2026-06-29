"""nature_basic_simulation.py

This module runs the nature simulation using the given entities"""
import random
import time
import yaml

from entities import Herbivore, Plant, Predator, Rock, Ground
from entities.mobile_entity import MobileEntity

ENTITY_MAP = {
    cls.SIGN: cls
    for cls in [Plant, Herbivore, Predator, Rock, Ground]
}

def load_config():
    """Loads the configuration from the config file"""
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def apply_config(config):
    """Insert YAML config values into entity class attributes."""
    Plant.t_plant = config.get("T_plant", Plant.t_plant)
    Herbivore.t_herbivore = config.get("T_herbivore", Herbivore.t_herbivore)
    Herbivore.r_herbivore_sight = config.get("R_herbivore_sight", Herbivore.r_herbivore_sight)
    Herbivore.t_cooldown = config.get("T_cooldown", Herbivore.t_cooldown)
    Predator.t_predator = config.get("T_predator", Predator.t_predator)
    Predator.r_predator_sight = config.get("R_predator_sight", Predator.r_predator_sight)


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
            if col is None:
                empty_cells.append((row_idx, col_idx))
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = Plant(r, c)

def move_entities(board: list):
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
             entity.step(board)

        spawn_random_plant(board)
        time.sleep(0.5)
    print_board(board)

def main():
    """Run the program"""
    config = load_config()
    apply_config(config)
    board = init_board()
    move_entities(board)


if __name__ == "__main__":
    main()
