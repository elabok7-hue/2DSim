"""Basic implementation of game of life."""
import time

ALIVE = "O"
DEAD = "."


def init_board(rows, cols):
    """Initializes board with dead cells."""
    return [[DEAD for c in range(cols)] for r in range(rows)]


def count_neighbour_live_cells(board: list, row: int, col: int):
    """Counts the number of living cells near a specified cell."""
    alive_counter = 0

    for check_row in range(row - 1, row + 2):
        if 0 <= check_row < len(board):
            for check_col in range(col - 1, col + 2):
                if 0 <= check_col < len(board[check_row]):
                    if board[check_row][check_col] == ALIVE:
                        alive_counter += 1

    if board[row][col] == ALIVE:
        alive_counter -= 1

    return alive_counter


def find_new_cell_status(cell: str, neighbours: int):
    """Finds the new status of the cell by the game of life rules."""
    # cell with 2 neighbors stays the same so its skipped
    if neighbours <= 1:
        cell = DEAD
    elif neighbours >= 4:
        cell = DEAD
    elif neighbours == 3:
        cell = ALIVE

    return cell


def update_board(board: list):
    """Updates the board to the new values according to the new cell status."""
    temp_board = []
    for idxI, row in enumerate(board):
        temp_row = []
        for idxJ, col in enumerate(row) :
            neighbours = count_neighbour_live_cells(board, idxI, idxJ)
            status = find_new_cell_status(board[idxI][idxJ], neighbours)
            temp_row.append(status)
        temp_board.append(temp_row)
    board = temp_board

    return board


def print_board(board: list):
    """Prints the board."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            print(board[row][col], end="")
        print()
    print()


def main():
    """Run the game of life."""
    with open("pulser.txt", "r") as f:
        board = [list(line.strip("\n")) for line in f]

    steps_counter = 0

    while steps_counter <= 15:
        print_board(board)
        board = update_board(board)
        time.sleep(0.5)
        steps_counter += 1

    print_board(board)


if __name__ == "__main__":
    main()
