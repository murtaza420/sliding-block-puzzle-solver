Steps to execute this project:


1. Download and install Python 3.7+ from https://www.python.org/downloads/
2. Install pip which is a package management system for python. The following link https://www.liquidweb.com/kb/install-pip-windows/
   will help you set up pip
3. Setting up a virtual environment is recommended but not necessary. If you do not wish to 
   set up, go to step 5
4. Run the following commands to setup and activate virtual environment: 
   python -m venv env
   .\env\Scripts\activate
5. Run the command to install all the dependencies:
   pip install -r requirements.txt
6. Run the command to start the web server:
   python run.py
7. In the browser, navigate to:
   http://localhost:8080/

You can now use the puzzle solver. If you are unfamiliar with the Sliding Block Puzzle, please refer to the ProblemStatement.pdf

Playing the game:
You can find sample inputs in src/input-examples/. Feel free to try your own puzzle too.
Make sure the regular blocks are numbered consecutively starting from 3.
For example: 3, 4, 6 is invalid as 5 is missing

In case you face any issues during the set up or execution of the project, please feel free to reach out to me on
murtazagodhrawala94@gmail.com