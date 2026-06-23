import time

ALIVE: int = 1
DEAD: int = 0

def init_board(rows, cols):
    board = []

    for row in range(rows):
        curr_row = []
        for col in range(cols):
            curr_row.append(DEAD)
        board.append(curr_row)

    board[2][3] = ALIVE
    board[2][4] = ALIVE
    board[2][5] = ALIVE

    return board

def count_neighbour_live_cells(board: list, row: int, col: int) -> int:
    alive_counter : int = 0

    for check_row in range(row - 1, row + 2):
        if 0 <= check_row < len(board):
            for check_col in range(col - 1, col + 2):
                if 0 <= check_col < len(board[check_row]):
                    if board[check_row][check_col] == ALIVE :
                        alive_counter += 1

    if board[row][col] == ALIVE:
        alive_counter -= 1

    return alive_counter

def find_new_cell_status(cell: int, neighbours: int):
    if neighbours <= 1:
        cell = DEAD
    elif neighbours >= 4:
        cell = DEAD
    elif neighbours == 3:
        cell = ALIVE

    return cell


def update_board(board: list):
    temp_board = []

    for row in range(len(board)):
        temp_row = []
        for col in range(len(board[row])):
            neighbours: int = count_neighbour_live_cells(board, row, col)
            status = find_new_cell_status(board[row][col], neighbours)
            temp_row.append(status)
        temp_board.append(temp_row)
    board = temp_board

    return board

def print_board(board: list):
    for row in range(len(board)):
        for col in range(len(board[row])):
            print(board[row][col], end=" ")
        print()
    print()

def check_all_dead(board: list):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == ALIVE:
                return False
    return True

def main():
    count = 0
    board = init_board(5, 6)

    while not check_all_dead(board):
        print_board(board)
        board = update_board(board)
        count +=1
        time.sleep(0.5)
    print_board(board)

main()