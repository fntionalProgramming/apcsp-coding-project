from random import randint
from copy import deepcopy
import array

class SudokuGenerator:
    def __doable(self, r: int, c: int, board: list[list[str]], target: str) -> bool:
        # Check if placing target in (r, c) is valid
        for i in range(len(board)):
            if board[r][i] == target or board[i][c] == target:
                return False
        start_row: int = r - r % 3
        start_col: int = c - c % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == target:
                    return False
        return True

    def __solveSudoku(self, board: list[list[str]]) -> bool:
        sdks: list[str] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        def solve(board: list[list[str]]) -> bool:
            r, c = -1, -1
            is_empty = True
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == ' ': 
                        r, c = i, j
                        is_empty = False
                        break
                if not is_empty:
                    break
            if is_empty:
                return True

            for ch in sdks:
                if self.__doable(r, c, board, ch):
                    board[r][c] = ch
                    if solve(board):
                        return True
                    board[r][c] = " "
            return False

        return solve(board)

    def generateSudoku(self, clues_lower_bound: int, clues_upper_bound) -> tuple[list[list[str]]]:
        counts: int = 6
        holes: int = randint(81-clues_upper_bound, 81-clues_lower_bound)
        # Start with an empty board using fixed-size array for rows and columns
        board: list[list[str]] = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
            [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
            [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " "], 
            [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        ]

        # Fill the board with a valid Sudoku solution
        positions: set[tuple[int, int]] = set()
        while counts > 0:
            new_row: int = randint(0, 8)
            new_col: int = randint(0, 8)
            if (new_row, new_col) not in positions:
                new_num: int = randint(1, 9)
                if self.__doable(new_row, new_col, board, str(new_num)):
                    positions.add((new_row, new_col))
                    board[new_row][new_col] = str(new_num)
                    counts -= 1

        # Solve the board to get a valid Sudoku puzzle
        if not self.__solveSudoku(board):
            return ([[]], [[]])
        solved_board: list[array.array] = deepcopy(board)

        # Now, punch holes
        while holes > 0:
            new_row: int = randint(0, 8)
            new_col: int = randint(0, 8)
            if board[new_row][new_col] != ' ': 
                # Backup the current cell
                backup: str = deepcopy(board[new_row][new_col])
                board[new_row][new_col] = ' '  
                new_board = deepcopy(board)

                # Check if the puzzle is still solvable
                if self.__solveSudoku(board):
                    board = new_board
                    holes -= 1
                else:
                    # If not solvable, revert the hole punch
                    board[new_row][new_col] = backup

        return (solved_board, board)

    def printBoard(self, board: list[list[str]]):
        for row in board:
            print(" ".join(row))

