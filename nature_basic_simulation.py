import random
import time
import yaml

from entities import Herbivore, Plant, Predator

PLANT_SIGN = "🍀"
HERBIVORE_SIGN = "🐔"
PREDATOR_SIGN = "🐺"
ROCK_SIGN = "🪨"
GROUND_SIGN = "🟫"


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def apply_config(config):
    """Insert yaml config values into entity class attributes."""
    Plant.t_plant = config.get("T_plant", Plant.t_plant)
    Herbivore.t_herbivore = config.get("T_herbivore", Herbivore.t_herbivore)
    Herbivore.r_herbivore_sight = config.get("R_herbivore_sight", Herbivore.r_herbivore_sight)
    Herbivore.t_cooldown = config.get("T_cooldown", Herbivore.t_cooldown)
    Predator.t_predator = config.get("T_predator", Predator.t_predator)
    Predator.r_predator_sight = config.get("R_predator_sight", Predator.r_predator_sight)


def init_board():
    """Initialize the board"""
    board = []

    with open("nature_board.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for row, line in enumerate(lines):
        line = line.strip()
        board_row = []
        col_index = 0
        for cell in line:
            if cell == PLANT_SIGN:
                board_row.append(Plant(row, col_index))
                col_index += 1
            elif cell == HERBIVORE_SIGN:
                board_row.append(Herbivore(row, col_index))
                col_index += 1
            elif cell == PREDATOR_SIGN:
                board_row.append(Predator(row, col_index))
                col_index += 1
            elif cell == ROCK_SIGN:
                board_row.append(ROCK_SIGN)
                col_index += 1
            elif cell == GROUND_SIGN:
                board_row.append(None)
                col_index += 1
        board.append(board_row)

    return board


def print_board(board: list):
    """Prints the board."""
    for row in board:
        for cell in row:
            if isinstance(cell, Plant):
                print(PLANT_SIGN, end="")
            elif isinstance(cell, Herbivore):
                print(HERBIVORE_SIGN, end="")
            elif isinstance(cell, Predator):
                print(PREDATOR_SIGN, end="")
            elif cell == ROCK_SIGN:
                print(ROCK_SIGN, end="")
            else:
                print(GROUND_SIGN, end="")
        print()
    print()


def spawn_random_plant(board : list):
    """Plants appear randomly at empty spaces."""

    empty_cells = []
    for row_idx, row in enumerate(board):
        for col_idx, col in enumerate(board[row_idx]):
            if board[row_idx][col_idx] is None:
                empty_cells.append((row_idx, col_idx))
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = Plant(r, c)


def main():
    config = load_config()
    apply_config(config)
    num_steps = 10
    board = init_board()

    for step in range(num_steps):
        print_board(board)
        entities_to_process = []

        for row in range(len(board)):
            for col in range(len(board[row])):
                cell = board[row][col]
                if isinstance(cell, (Plant, Herbivore, Predator)):
                    entities_to_process.append(cell)

        for entity in entities_to_process:
            if isinstance(entity, Predator):
                if board[entity.row][entity.col] is entity:
                    entity.predator_step(board)

        for entity in entities_to_process:
            if isinstance(entity, Herbivore):
                if board[entity.row][entity.col] is entity:
                    entity.herbivore_step(board)

        for entity in entities_to_process:
            if isinstance(entity, Plant):
                if board[entity.row][entity.col] is entity:
                    entity.plant_step(board)

        spawn_random_plant(board)
        time.sleep(0.5)

    print_board(board)


if __name__ == "__main__":
    main()
