from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import sys, os, json

# puzzle_solver_path = "./src/puzzle_solver"
# sys.path.append(os.path.abspath(puzzle_solver_path))
from src.puzzle_solver import BrickPuzzle


app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/solve_puzzle', methods=['GET', 'POST'])
def solve_puzzle():
    print('HEEELEOOO')
    if request.method == 'POST':
        data = request.get_json()
    
        puzzle = BrickPuzzle()
        puzzle.setInitialState(data)
        output = puzzle.solve()

    print(output)

    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

def validDimensions(dimensions):
    dim = dimensions.split(',')
    if(len(dim) != 2):
        return False
    return True

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)