from flask import Flask, render_template, request, jsonify, redirect, url_for
from sudokuSolver import SudokuGenerator
from typing import List

app = Flask(__name__, template_folder="templates")
# storing the current solution
solution: List[List[str]]= [[None]]
SDK_ROW_SIZE: int = 9
SDK_COL_SIZE: int = 9

# the main route
@app.route("/")
def main():
   return render_template("main.html")

# function for creating a new board when a button is clicked
@app.route("/generate", methods=["POST"])
def generateSudoku():
    global solution
    # get the clue counts from the data sended from the front end
    clue_counts =  request.get_json().get("clueCount")
    # generate the sudokus
    sdk = SudokuGenerator()
    # get the solution and the unsolved board itself
    solution, unsolved_board = sdk.generateSudoku(clue_counts, clue_counts)
    # return a response of the unsolved board and the default number of retries
    return jsonify({"unsolved_board": unsolved_board, "retries": 3})


# function for rendering the board
@app.route('/board')
def board():
    return render_template("board.html")


# function for validating the board
@app.route("/validate", methods=["POST"])
def validate_sudoku():
    # get the current board and the current retries that is sent from the client
    data = request.get_json()
    current_board = data["current_board"]
    retries = data["retries"]
    # check if the current board matches the solution
    for i in range(SDK_ROW_SIZE):
        for j in range(SDK_COL_SIZE):
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

# function for rendering the failed page
@app.route('/failed')
def failed():
    return render_template("failed.html")

# function for rending the win page
@app.route('/success')
def success():
    return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=True)



