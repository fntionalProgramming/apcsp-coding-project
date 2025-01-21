from random import randint # for random number
from copy import deepcopy # for making a deepcopy

'''
    module for generating the sudoku
    example:
    clues_lower_bound = 30
    clues_upper_bound = 36
    sdk = SudokuGenerator
    try:
        solved_board, unsolved_board = sdk.generateSudoku()
    catch SudokuSolverError as e:
        print(e)
'''
'''
    exception class
'''
class SudokuSolveError(Exception):
    '''
        function that initilize a error message
    '''
    def __init__(self, message):
        super().__init__(message)

class SudokuGenerator:
    '''
    doable function check if a nubmer can be there in a board by check for the column and the row and the subgrid is a number already exits
    '''
    def __doable(self, r: int, c: int, board: list[list[str]], target: str) -> bool:
        # Check for the row and column if the number already exits, if the number already exits then return false immidiately
        for i in range(len(board)):
            if board[r][i] == target or board[i][c] == target:
                return False
        # get the start column and row index of the subgrid this work by
        '''
            imagine the columns on the sudoku
            0 1 2 3 4 5 6 7 8

            when you mode the current column by 3 for example
            0 % 3 = 0
            1 % 3 = 1
            2 % 3 = 2

            3 % 3 = 0
            4 % 3 = 1
            5 % 3 = 2

            6 % 3 = 0
            7 % 3 = 1
            8 % 3 = 2

            we can see by modding by 3 we can divide the grid in to three subgrid
            but we dont know which subgrid is which subgrid 
            but if we minus the current col index by the modulo result we can actually know what subgrid where are at
            for example
            first sub grid
            0 - 0 = 0 
            1 - 1 = 0
            2 - 2 = 0  
            second sub grid
            3 - 0 = 3
            4 - 1 = 3
            5 - 2 = 3
            third subgrid
            6 - 0 = 6
            7 - 1 = 6
            8 - 1 = 6 
            this is how the math work and this also ork the same for the row index because a sudoku is defined by a 9 by 9 grid
        '''
        start_row: int = r - r % 3
        start_col: int = c - c % 3
        # iterate until the end of each sub grid and check if the number we want to put in already exits
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == target:
                    return False
        # return true if passess all the check to indicate that we can put the number there
        return True

    # function for solving the sudoku
    '''
        function takes in a 9x9 board and solve the sudoku
    '''
    def __solveSudoku(self, board: list[list[str]]) -> bool:
        sdks: list[str] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        # sub function for recursively solving the sudoku
        '''
            this is the actually function that uses backtracking to solve the sudoku
        '''
        def solve(board: list[list[str]]) -> bool:
            # empty initilization and current row and column
            r = -1
            c = -1
            # iterate until the firrst empty slow which we wil ater try to recursively solve
            is_empty = True
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == ' ': 
                        r, c = i, j
                        is_empty = False
                        break
                if not is_empty:
                    break
            # return true when isempty is true because this mean the board is solved or already been solved
            if is_empty:
                return True
            # iterate over all the options we have for that slot
            for ch in sdks:
                # check if we cnan put that character at that slot
                if self.__doable(r, c, board, ch):
                    # if indeed we can put that character put that character
                    board[r][c] = ch
                    # recursively try to solve the board  if in while solving we solved the board immideiately return true
                    if solve(board):
                        return True
                    # backtracking, undoing our move
                    board[r][c] = " "
            # trigger the backtracking by returning the reason we return false because the board is still not solved yet
            return False
        # solve the board
        return solve(board)
    '''
        function follow the steps of generting sudoku board is this https://zhangroup.aporc.org/images/files/Paper_3485.pdf
        the first step is to init a empty board
        the second step is to sprinkle on some numbers which is 6 because statisticly generating a sudoku with 6 valid numbers
        yield a near 100% of a solvable sudoku
        the third step is to solve the spinkled board if it is not solvable raise an exception (which is really rare)
        the last step is to punch some valid holes by checking if the board is solvable when punching a hole
    '''
    def generateSudoku(self, clues_lower_bound: int, clues_upper_bound) -> tuple[list[list[str]]]:
        # the reason we check for less than 17 because mathmatically is the minimum clues for a 
        # sudoku to have atleast one solution
        if clues_lower_bound < 17 or clues_upper_bound < 17:
            raise SudokuSolveError("Clues must be atleast 17")
        # sudoku only have 81 cells so we have to check are the clues smaller than 81 if not then raise an exception
        if clues_lower_bound > 81 or clues_upper_bound > 81:
            raise SudokuSolveError("Clues must be less than 81")
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
        # keep track of the posisiont we just insert holes in 
        positions: set[tuple[int, int]] = set()
        # iterate until we succesfully sprinkle on 6 random valid numbews 
        while counts > 0:
            # get the random coordinates for sprinkle on
            new_row: int = randint(0, 8)
            new_col: int = randint(0, 8)
            # only sprinkle number if we have not seedn teh coordinates yet
            if (new_row, new_col) not in positions:
                # get a random number for sprinkiling
                new_num: int = randint(1, 9)
                # check if we can put the number there
                if self.__doable(new_row, new_col, board, str(new_num)):
                    # if we can put the number there then we add them to our seen set to indicate we already seen those number
                    positions.add((new_row, new_col))
                    #insert the number on to the board
                    board[new_row][new_col] = str(new_num)
                    # decrease the count to indicate that we have sprinkle on one number
                    counts -= 1
        # extremely rare because the possibility for sprinkiling 6 numbers and ensuring a working suduoku is near 100%, around 99.99999999%
        # but if there is a error generating the board we raise a exception
        if not self.__solveSudoku(board):
            raise SudokuSolveError("Error solving the Sudoku board")
        # make a deep copy, this wil be our solutions the reaso n we do a deep copy because python modify stuff by reference
        # so when we punch the holes the later on it wil modify the refernece and destroyed our solved board
        solved_board: list[list[str]] = deepcopy(board)
        # now we punch the holes
        # the logic of this code is pretty much like the sprinkling on number but a little bit of a different in the internal logic
        while holes > 0:
            new_row: int = randint(0, 8)
            new_col: int = randint(0, 8)
            if board[new_row][new_col] != ' ': 
                '''
                    the reason we make a deep copy of the current board is because if we dont
                    for some reason of how python do thing with references when we return the punch holes board
                    we wont get any holes punched
                '''
                # backup the current cell and the current board for later copy
                backup: str = deepcopy(board[new_row][new_col])
                board[new_row][new_col] = ' '  
                new_board = deepcopy(board)

                # chekc if the puzzle is still solvable after we punched holes
                if self.__solveSudoku(board):
                    # if the board is still solvable make the current board the backup board and decrease holes to indicate that we punched a hole
                    board = new_board
                    holes -= 1
                else:
                    # If not solvable, revert the hole punch
                    board[new_row][new_col] = backup
            # skip the cell we already punch holes
        # return the solved board and the unsolved board
        return (solved_board, board)
    '''
        function for printing the board
    '''
    def printBoard(self, board: list[list[str]]):
        for row in board:
            # print the board after a new end line
            print(row + '\n')

    

