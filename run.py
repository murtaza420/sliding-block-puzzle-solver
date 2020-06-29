from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import sys, os, json
from src.puzzle_solver import BrickPuzzle


app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/solve_puzzle', methods=['GET', 'POST'])
def solve_puzzle():
    if request.method == 'POST':
        data = request.get_json()
    
        puzzle = BrickPuzzle()
        puzzle.setInitialState(data)
        output = puzzle.solve()

        bfsOutput = formatOutput(output[0])
        dfsOutput = formatOutput(output[1])
        idfsOutput = formatOutput(output[2])

        output = {
            'bfs': bfsOutput,
            'dfs': dfsOutput,
            'idfs': idfsOutput
        }
        resp = jsonify(output)
        resp.status_code = 200
        return resp
        # return render_template('results.html', bfs=bfsOutput, dfs=dfsOutput, idfs=idfsOutput)
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

def validDimensions(dimensions):
    dim = dimensions.split(',')
    if(len(dim) != 2):
        return False
    return True

def formatOutput(output):
    moves = []
    time = 0
    final_state = {}

    count = 1
    lines = output.split('\n')
    for line in lines:
        # print(line)
        if '(' in line:
            moves.append(line)
        elif ',' in line:
            elements = line.split(',')
            for e in elements:
                if e is not '':
                    final_state[str(count)] = int(e)
                    count += 1
        elif len(line) > 1:
            time = float(line.split(' ')[1])

    return {
        'moves': moves,
        'time': time,
        'final_state': final_state
    }


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)