from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import os, json

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/solve_puzzle', methods=['GET', 'POST'])
def solve_puzzle():
    print('HEEELEOOO')
    if request.method == 'POST':
        data = request.get_json()
        print(data['dimensions'])
        # dimensions = request.form['dimensions']
        # # print(dimensions)
        # if(not validDimensions(dimensions)):
        #     return render_template('index.html', error="Invalid Dimensions")

        # [x, y] = dimensions.split(',')
        # print(x)
        # print(y)

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