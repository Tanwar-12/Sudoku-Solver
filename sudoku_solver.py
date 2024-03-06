import sys
from time import sleep
import os
import argparse


def clear_screen():
    """Clear terminal.
    """
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def clear_lines(n):
    """Move the cursor up `n` lines and clear those lines.

    Args:
        n (int): Number of lines to clear.
    """
    for _ in range(n):
        sys.stdout.write('\x1b[1A')  # Move cursor up by one line
        sys.stdout.write('\x1b[2K')  # Clear the line


def print_sudoku(sudoku):
    """Displays the Sudoku in the terminal.

    Args:
        sudoku (list(list(int))): List of lists containing the sudoku.
    """
    clear_lines(11)

    for i, row in enumerate(sudoku):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")

        row_str = ""
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += f"{cell if cell != 0 else ' '} "

        print(row_str.rstrip())  # Print the row and remove any trailing spaces


def get_sudoku_from_file(file_path):
    """Get sudoku from a text file and converts it into a list of lists.

    Args:
        file_path (srt): File path.

    Returns:
        sudoku (list(list(int))): List of lists containing the sudoku.
    """
    sudoku = []
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            sudoku_line = []
            for number in line:
                sudoku_line.append(int(number))
            sudoku.append(sudoku_line)

    return sudoku


def is_valid(sudoku, r, c, value):
    """Returns True if the given value is a feasible solution at the given row and column.
    It checks the if the number is already in the full row, full column and full sub-box.

    Args:
        sudoku (list(list(int))): List of lists containing the sudoku.
        r (int): Sudoku's row.
        c (int): Sudoku's column.
        value (int): Value to check.

    Returns:
        bool: True if value is a feasible solution at the given location.
    """

    if value in sudoku[r]:
        return False

    for row in range(9):
        if value == sudoku[row][c]:
            return False

    square_row = r // 3
    square_column = c // 3

    for row in range(9):
        for column in range(9):
            if (row // 3) == square_row and (column // 3) == square_column:
                if sudoku[row][column] == value:
                    return False

    return True


def solve(sudoku, r=0, c=0, visualize=False):
    """Recursive brute force sudoku solver.

    Args:
        sudoku (list(list(int))): List of lists containing the sudoku.
        r (int, optional): Sudoku's row. Defaults to 0.
        c (int, optional): Sudoku's column. Defaults to 0.
        visualize (bool, optional): If True shows the solving process in the terminal. Defaults to False.

    Returns:
        bool: True if solution found.
    """

    if visualize:
        print_sudoku(sudoku)
        sleep(0.001)

    next_c = c + 1
    next_r = r
    if next_c == 9:
        next_c = 0
        next_r = r + 1

    if sudoku[r][c] == 0:
        none_valid = True
        for value in range(1, 10):
            if is_valid(sudoku, r, c, value):
                none_valid = True
                sudoku[r][c] = value
                if r == 8 and c == 8:
                    return True
                result = solve(sudoku, next_r, next_c, visualize)
                if not result:
                    sudoku[r][c] = 0
                else:
                    return result
        if none_valid:
            return False
    else:
        if r == 8 and c == 8:
            return True
        return solve(sudoku, next_r, next_c, visualize)


def main():
    try:

        parser = argparse.ArgumentParser(
            description=
            "Sudoku Solver (9x9). Define the Sudoku to be solved in .txt file. Setting the unknown numbers as zeroes,\
                every row in a different line, and no separation for the columns."
        )
        parser.add_argument(
            '-p',
            '--path',
            type=str,
            default='sudoku.txt',
            help='Path to the .txt file with the Sudoku. Default: sudoku.txt')
        parser.add_argument(
            '-v',
            '--visualize',
            action='store_true',
            help='Visualize the solving process. Default: False')
        args = parser.parse_args()

        clear_screen()
        sudoku = get_sudoku_from_file(args.path)
        solve(sudoku, visualize=args.visualize)
        print_sudoku(sudoku)

    except KeyboardInterrupt as e:
        print(f"Program interrupted with the Keyboard! {e}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
