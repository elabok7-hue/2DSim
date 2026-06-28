import random
import time

import yaml
from entities import Herbivore, Plant, Predator

plant_sign = "🍀"
herbivore_sign = "🐔"
predator_sign = "🐺"
rock_sign = "🪨"
ground = "🟫"


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
            if cell == plant_sign:
                board_row.append(Plant(row, col_index))
                col_index += 1
            elif cell == herbivore_sign:
                board_row.append(Herbivore(row, col_index))
                col_index += 1
            elif cell == predator_sign:
                board_row.append(Predator(row, col_index))
                col_index += 1
            elif cell == rock_sign:
                board_row.append(rock_sign)
                col_index += 1
            elif cell == ground:
                board_row.append(None)
                col_index += 1
        board.append(board_row)

    return board


def print_board(board: list):
    """Prints the board."""
    for row in board:
        for cell in row:
            if isinstance(cell, Plant):
                print(plant_sign, end="")
            elif isinstance(cell, Herbivore):
                print(herbivore_sign, end="")
            elif isinstance(cell, Predator):
                print(predator_sign, end="")
            elif cell == rock_sign:
                print(rock_sign, end="")
            else:
                print("🟫", end="")
        print()
    print()


def move_entity_on_board(entity, old_row: int, old_col: int, board: list):
    """Update the board after an entity changed position."""

    if board[old_row][old_col] is entity:
        board[old_row][old_col] = None

    if 0 <= entity.row < len(board) and 0 <= entity.col < len(board[0]):
        board[entity.row][entity.col] = entity


def remove_from_board(entity, board: list):
    """Remove an entity from the board."""
    if board[entity.row][entity.col] is entity:
        board[entity.row][entity.col] = None


def plant_step(curr_plant: Plant, board: list):
    """Implements plant functionality."""
    curr_plant.increase_age()
    if curr_plant.is_dead():
        remove_from_board(curr_plant, board)


def herbivore_step(curr_herbivore: Herbivore, board: list):
    """Implements herbivore functionality."""
    curr_herbivore.increase_age()

    if curr_herbivore.is_dead():
        remove_from_board(curr_herbivore, board)
    else:

        old_row, old_col = curr_herbivore.row, curr_herbivore.col

        if curr_herbivore.can_reproduce():
            partner = curr_herbivore.find_nearest_herbivore(board)

            if partner is not None:
                baby = curr_herbivore.reproduce(board)

                if baby:
                    board[baby.row][baby.col] = baby

                curr_herbivore.cooldown_timer = curr_herbivore.t_cooldown
                partner.cooldown_timer = partner.t_cooldown
                return

        nearest_plant = curr_herbivore.find_nearest_plant(board)
        if nearest_plant is None:
            curr_herbivore.move_randomly(board)
        else:
            curr_herbivore.move_towards_plant(nearest_plant)

        move_entity_on_board(curr_herbivore, old_row, old_col, board)
        target = board[curr_herbivore.row][curr_herbivore.col]

        if isinstance(target, Plant) and target is not curr_herbivore:
            remove_from_board(target, board)
            curr_herbivore.refuel_life_span()
        board[curr_herbivore.row][curr_herbivore.col] = curr_herbivore


def predator_step(curr_predator: Predator, board: list):
    """Implemets predator functionality."""
    curr_predator.increase_age()

    if curr_predator.is_dead():
        remove_from_board(curr_predator, board)
    else:

        old_row, old_col = curr_predator.row, curr_predator.col

        nearest_herbivore = curr_predator.find_nearest_herbivore(board)
        if nearest_herbivore is None:
            curr_predator.move_randomly(board)
        else:
            curr_predator.move_towards_herbivore(nearest_herbivore)

        move_entity_on_board(curr_predator, old_row, old_col, board)

        target = board[curr_predator.row][curr_predator.col]

        if isinstance(target, Herbivore):
            remove_from_board(target, board)
            curr_predator.refuel_life_span()
        elif isinstance(target, Plant):
            remove_from_board(target, board)

        board[curr_predator.row][curr_predator.col] = curr_predator


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
                    predator_step(entity, board)

        for entity in entities_to_process:
            if isinstance(entity, Herbivore):
                if board[entity.row][entity.col] is entity:
                    herbivore_step(entity, board)

        for entity in entities_to_process:
            if isinstance(entity, Plant):
                if board[entity.row][entity.col] is entity:
                    plant_step(entity, board)

        spawn_random_plant(board)
        time.sleep(0.5)

    print_board(board)


if __name__ == "__main__":
    main()
