from flask import Flask, render_template, request, jsonify, redirect, url_for # import nesscessary functions
from sudokuSolver import SudokuGenerator, SudokuSolveError # import the sudoku generator and the error type

'''
    flask backend to to stuff like rendering pages and validate the sudoku
'''
# init flask application
app = Flask(__name__, template_folder="templates")
# storing the curretn solution
solution: List[List[str]]= [[None]]
# some constant for the size of the board because it wont be changing
SDK_ROW_SIZE: int = 9
SDK_COL_SIZE: int = 9

'''
    function for rending the main page
'''
@app.route("/")
def main():
    return render_template("main.html")

'''
    end point for generating the board
'''
@app.route("/generate", methods=["POST"])
def generateSudoku():
    global solution
    # get the clue counts from the data sended from the front end
    clue_counts =  request.get_json().get("clueCount")
    # generate the sudokus
    sdk = SudokuGenerator()
    # get the solution and the unsolved board itself
    try:
        # if we can solved the sudoku board then we are good
        solution, unsolved_board = sdk.generateSudoku(clue_counts, clue_counts)
        return jsonify({"unsolved_board": unsolved_board, "retries": 3})
    except SudokuSolveError as e:
        return jsonify({"unsolved_board": "Unsolvable", "retries": 0})

'''
    route for rendering the board layout from board.html
'''
@app.route('/board')
def board():
    return render_template("board.html")


'''
    end point for validating the current board which will b sent from the front end
'''
@app.route("/validate", methods=["POST"])
def validate_sudoku():
    # get the current board and the current retries that is sent from the client
    data = request.get_json()
    current_board = data["current_board"]
    retries = data["retries"]
    # check if the current board matches the solution
    # iterate until SDKROWSIZE and SDKCOLSIZE because our sudoku dont change throughout so we do not always need to get the size of the board
    for i in range(SDK_ROW_SIZE):
        for j in range(SDK_COL_SIZE):
            # check if the boad is incomplete or the cell doesnot match with the answers
            if solution[i][j] != current_board[i][j] or current_board[i][j] == ' ':
                if retries - 1 == 0:
                    # if the user failed redirect to failed page
                    return redirect(url_for("failed"))
                else:
                    # decrment retries send back to the front end
                    retries -= 1
                    return jsonify({"retries": retries})

    # redirect to success if we pass all check s
    return redirect(url_for("success"))

'''
    endpoint for rendering the lost screen from failed.html
'''
@app.route('/failed')
def failed():
    return render_template("failed.html")

'''
    endpoint for rendering the win screen from succcess.html
'''
@app.route('/success')
def success():
    return render_template("success.html")

'''
    maain function to run the app
'''
if __name__ == '__main__':
    # run wit debug=True if only in development
    app.run(debug=False)



