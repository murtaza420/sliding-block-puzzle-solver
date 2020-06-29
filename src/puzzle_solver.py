import random
import time

class BrickPuzzle:

    def __init__(self):
        self.initial_game_state = []

        # Stores all the game states. List of Matrix
        self.game_states = []

        # Stores all possible moves from a state, List is of tuple. For eg: [(2, 'left'),(3, 'left')]
        self.possible_moves = []

        # Stores all possible union of moves of each block from a state 
        self.possible_moves_union = {}

        # Stores positions of 0's
        self.blanks_positions = [] 

        # Stores positions of -1's
        self.goal_positions = []

        # Stores positions and dimensions of blocks > 1
        self.block_details = {}

        self.union_move_visited = {}
        self.bfs_queue = []
        self.dfs_queue = []
        self.idfs_queue = []
        self.dfs_puzzle_solved = False
        self.idfs_puzzle_solved = False
        self.dfs_counter = 0
        self.bfsOutput = ""
        self.dfsOutput = ""
        self.idfsOutput = ""

    def setInitialState(self, data):
        
        dimensions = data['dimensions'].split(",")
        no_of_columns = int(dimensions[0])
        no_of_rows = int(dimensions[1])

        self.initial_game_state = [[0 for i in range(no_of_columns)] for j in range(no_of_rows)]
        element = 1
        # Reads the game state and stores blank positions, goal positions and block details
        for i in range(no_of_rows):
            for j in range(no_of_columns):
                self.initial_game_state[i][j] = int(data[str(element)])
                element += 1
                if(self.initial_game_state[i][j] == 0):
                    # Blank positions
                    self.blanks_positions.append((i,j))
                elif self.initial_game_state[i][j] == -1:
                    # Goal positions
                    self.goal_positions.append((i,j))
                elif self.initial_game_state[i][j] > 1:
                    # Block details
                    if not self.initial_game_state[i][j] in self.block_details:
                        self.block_details.update({self.initial_game_state[i][j] : BlockDetails(1,(1,1),[(i,j)])})
                    else:
                        # Stores the total number of blocks with same number (Eg: 1, 2, 4,..etc)
                        self.block_details[self.initial_game_state[i][j]].block_count += 1
                        # Stores the position of each block with the same number
                        self.block_details[self.initial_game_state[i][j]].block_position_list.append((i,j))


        self.initial_game_state = self.normalizeState(self.initial_game_state)
        self.game_states.append(self.initial_game_state.copy())
        self.bfs_queue.append(self.initial_game_state.copy())
        self.dfs_queue.append(self.initial_game_state.copy())
        self.idfs_queue.append(self.initial_game_state.copy())

    def printGameState(self, game_state):
        output = ""
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                # print(game_state[i][j],end=',')
                output += str(game_state[i][j]) + ','
            output += "\n"
            # print()
        return output

    def solve(self):
        # BFS
        t1 = time.perf_counter()
        nodes = self.bfs(0)
        t2 = time.perf_counter()
        self.bfsOutput += str(nodes) + " " + str(round(t2-t1,2)) + " " + str(nodes - 1) +"\n"
        
        # DFS
        t1 = time.perf_counter()
        nodes = self.dfs()
        t2 = time.perf_counter()
        self.dfsOutput += str(nodes) + " " + str(round(t2-t1,2)) + " " + str(nodes - 1) +"\n"
        
        # IDFS
        idfs_counter = 1
        t1 = time.perf_counter()
        # Keep incrementing depth value till puzzle is solved
        while(not self.idfs_puzzle_solved):
            nodes = self.idfs(idfs_counter)
            idfs_counter += 1
        t2 = time.perf_counter()
        self.idfsOutput += str(nodes) + " " + str(round(t2-t1,2)) + " " + str(nodes - 1)
        
        return [self.bfsOutput, self.dfsOutput, self.idfsOutput]

    def isPuzzleSolved(self, game_state):
        print
        for i in game_state:
            if -1 in i:
                return False
        return True

    def generatePossibleMoves(self, game_state):
        self.possible_moves.clear()
        self.checkGoalMove(game_state)
        
        # Find all the moves based on adjacency to '0' blocks
        block_move_flag = True
        for i,j in self.blanks_positions:
            if(game_state[i-1][j] > 1 and not (game_state[i-1][j],'down') in self.possible_moves):
                # If Block size is greater than 1, check if the whole block can be moved
                if(self.block_details[game_state[i-1][j]].block_count > 1):
                    for k in self.block_details[game_state[i-1][j]].block_position_list:
                        # Don't generate the move if adjacent blocks are not with the same number and a block other than '0'
                        # > 1 condition is given as -1 (Goal State) has been checked and 1 is a wall
                        if(not game_state[k[0]+1][k[1]] == game_state[k[0]][k[1]] and game_state[k[0]+1][k[1]] > 1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i-1][j],'down'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i-1][j],'down'))
            if(game_state[i+1][j] > 1 and not (game_state[i+1][j],'up') in self.possible_moves):
                if(self.block_details[game_state[i+1][j]].block_count > 1):
                    for k in self.block_details[game_state[i+1][j]].block_position_list:
                        if(not game_state[k[0]-1][k[1]] == game_state[k[0]][k[1]] and game_state[k[0]-1][k[1]] > 1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i+1][j],'up'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i+1][j],'up'))
            if(game_state[i][j+1] > 1 and not (game_state[i][j+1],'left') in self.possible_moves):
                if(self.block_details[game_state[i][j+1]].block_count > 1):
                    for k in self.block_details[game_state[i][j+1]].block_position_list:
                        if(not game_state[k[0]][k[1]-1] == game_state[k[0]][k[1]] and game_state[k[0]][k[1]-1] > 1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i][j+1],'left'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i][j+1],'left'))
            if(game_state[i][j-1] > 1 and not (game_state[i][j-1],'right') in self.possible_moves):
                if(self.block_details[game_state[i][j-1]].block_count > 1):
                    for k in self.block_details[game_state[i][j-1]].block_position_list:
                        if(not game_state[k[0]][k[1]+1] == game_state[k[0]][k[1]] and game_state[k[0]][k[1]+1] > 1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i][j-1],'right'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i][j-1],'right'))

    def checkGoalMove(self, game_state):
        block_move_flag = True
        for i,j in self.goal_positions:
            # Goal moves are checked based on block 2 (Master Block)
            # Boundary conditions are checked to avoid array out of bound exception
            if((i - 1) >= 0 and game_state[i-1][j] == 2 and not (game_state[i-1][j],'down') in self.possible_moves):
                if(self.block_details[game_state[i-1][j]].block_count > 1):
                    # Master block size > 1, whole blocked is checked for generation of move
                    for k in self.block_details[game_state[i-1][j]].block_position_list:
                        if(not game_state[k[0]+1][k[1]] == game_state[k[0]][k[1]] and game_state[k[0]+1][k[1]] != -1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i-1][j],'down'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i-1][j],'down'))
            if((i < len(game_state) - 1) and game_state[i+1][j] == 2 and not (game_state[i+1][j],'up') in self.possible_moves):
                if(self.block_details[game_state[i+1][j]].block_count > 1):
                    for k in self.block_details[game_state[i+1][j]].block_position_list:
                        if(not game_state[k[0]-1][k[1]] == game_state[k[0]][k[1]] and game_state[k[0]-1][k[1]] != -1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i+1][j],'up'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i+1][j],'up'))
            if((j < len(game_state[i]) - 1) and game_state[i][j+1] == 2 and not (game_state[i][j+1],'left') in self.possible_moves):
                if(self.block_details[game_state[i][j+1]].block_count > 1):
                    for k in self.block_details[game_state[i][j+1]].block_position_list:
                        if(not game_state[k[0]][k[1]-1] == game_state[k[0]][k[1]] and game_state[k[0]][k[1]-1] != -1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i][j+1],'left'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i][j+1],'left'))
            if((j - 1) >= 0 and game_state[i][j-1] == 2 and not (game_state[i][j-1],'right') in self.possible_moves):
                if(self.block_details[game_state[i][j-1]].block_count > 1):
                    for k in self.block_details[game_state[i][j-1]].block_position_list:
                        if(not game_state[k[0]][k[1]+1] == game_state[k[0]][k[1]] and game_state[k[0]][k[1]+1] != -1):
                            block_move_flag = False
                            break
                    if(block_move_flag):
                        self.possible_moves.append((game_state[i][j-1],'right'))
                    else:
                        block_move_flag = True
                else:
                    self.possible_moves.append((game_state[i][j-1],'right'))

    def applyMove(self, game_state,move):
        # Creates a blank state
        new_state = [[0 for j in range(len(game_state[i]))] for i in range(len(game_state))]
        # Applies the move
        # Eg: if 3 is at [i][j] and the move is right, 3 is assigned [i][j+1]
        # Here, i[0] signifies the row and i[1] signifies the column 
        if(move[1] == 'right'):
            for i in self.block_details[move[0]].block_position_list:
                new_state[i[0]][i[1]+1] = move[0]
        elif(move[1] == 'left'):
            for i in self.block_details[move[0]].block_position_list:
                new_state[i[0]][i[1]-1] = move[0]
        elif(move[1] == 'up'):
            for i in self.block_details[move[0]].block_position_list:
                new_state[i[0]-1][i[1]] = move[0]
        elif(move[1] == 'down'):
            for i in self.block_details[move[0]].block_position_list:
                new_state[i[0]+1][i[1]] = move[0]

        # Fills the rest of the blocks except the move block
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                if(game_state[i][j] != move[0] and new_state[i][j] == 0):
                    new_state[i][j] = game_state[i][j]

        #updateBlankPositions(new_state)
        return new_state

    # Updates the blank positions after a applying a move
    def updateBlankPositions(self, game_state):
        self.blanks_positions.clear()
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                if(game_state[i][j] == 0):
                    self.blanks_positions.append((i,j))

    # Updates block dimensions after normalising
    # Block 5 of 1X1 can become 2X1 after normalisation
    def updateBlockDimensions(self):
        for i in self.block_details:
            # Subtracts the first and last blocks of the same number in the matrix
            self.block_details[i].block_dimension = (abs(self.block_details[i].block_position_list[-1][0] - self.block_details[i].block_position_list[0][0] + 1), 
            abs(self.block_details[i].block_position_list[-1][1] - self.block_details[i].block_position_list[0][1] + 1))

    # Updates the block counts and their positions
    def updateBlockDetails(self, game_state):
        for i in self.block_details:
            self.block_details[i].block_position_list.clear()
            self.block_details[i].block_count = 0

        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                if(game_state[i][j] > 1):
                    self.block_details[game_state[i][j]].block_position_list.append((i,j))
                    self.block_details[game_state[i][j]].block_count += 1
                    
    # Replaces the block numbers > 3 in ascending order to avoid visiting similar state structures again
    def normalizeState(self, game_state):
        k = 3
        normalised_mapping = {}
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                if(game_state[i][j] > 2):
                    if(not game_state[i][j] in normalised_mapping):
                        normalised_mapping.update({game_state[i][j]:k})
                        k += 1
                    game_state[i][j] = normalised_mapping[game_state[i][j]]
                    #print(j)
        self.updateBlockDetails(game_state)
        self.updateBlockDimensions()
        self.updateBlankPositions(game_state)

        return game_state

    def dfs(self):
        # global dfs_puzzle_solved
        # List of moves corresponding to the states
        dfs_moves = []
        # Initialise the stack with root state
        dfs_stack = self.dfs_queue.copy()
        n = 0
        # global self.output
        while(True):
            # Doesn't pop move for the root state
            if(len(dfs_moves) > 0):
                move_taken = dfs_moves.pop()
                # print(str(move_taken))
                self.dfsOutput += str(move_taken) + "\n"
            # Pops out the state on top of the stack (Last entered state)
            game_state = dfs_stack.pop()
            # Updates blank positions and blocks details for move generation
            self.updateBlockDetails(game_state)
            self.updateBlockDimensions()
            self.updateBlankPositions(game_state)
            # Generates all possible moves
            self.generatePossibleMoves(game_state)
            # Applies all the moves and only adds it in the stack if it is not visited
            for move in self.possible_moves.copy():
                # Updates blank positions and block with respect to current state as blank positions and block details will change
                # after applying every move
                self.updateBlockDetails(game_state)
                self.updateBlockDimensions()
                self.updateBlankPositions(game_state)
                new_state = self.applyMove(game_state,move)
                new_state = self.normalizeState(new_state)
                # Adds the state in the stack and the corresponding move only if state not visited and puzzle not solved
                if(not new_state in self.dfs_queue and not self.dfs_puzzle_solved):
                    self.dfs_queue.append(new_state)
                    dfs_stack.append(new_state)
                    dfs_moves.append(move)
                    # If puzzle solved i.e. search complete, breaks the loop
                    if(self.isPuzzleSolved(new_state)):
                        self.dfs_puzzle_solved = True
                        # print(str(move))
                        self.dfsOutput += str(move) + "\n"
                        self.dfsOutput += self.printGameState(new_state)
                        break
            if self.dfs_puzzle_solved:
                break
            n += 1
        return len(self.dfs_queue) - len(dfs_stack)

    def idfs(self, depth):
        idfs_stack = []
        idfs_moves = []
        # Add depth 1 as root is visited
        idfs_depth = [1]
        self.idfs_queue.clear()
        self.idfs_queue.append(self.initial_game_state.copy())
        idfs_stack = self.idfs_queue.copy()
        # Only last iteration moves printed in output file
        output1 = ""
        # Iterate till stack has any states
        while(idfs_stack):
            if(len(idfs_moves) > 0):
                move_taken = idfs_moves.pop()
                # print(str(move_taken))
                output1 += str(move_taken) + "\n"
            # Pop out the top element of the stack
            game_state = idfs_stack.pop()
            current_depth = idfs_depth.pop()
            self.updateBlockDetails(game_state)
            self.updateBlockDimensions()
            self.updateBlankPositions(game_state)
            self.generatePossibleMoves(game_state)
            for move in self.possible_moves.copy():
                self.updateBlockDetails(game_state)
                self.updateBlockDimensions()
                self.updateBlankPositions(game_state)
                new_state = self.applyMove(game_state,move)
                new_state = self.normalizeState(new_state)
                # Similar to DFS, just stop when depth is reached
                if(not new_state in self.idfs_queue and not self.idfs_puzzle_solved and current_depth < depth):
                    self.idfs_queue.append(new_state)
                    idfs_stack.append(new_state)
                    idfs_moves.append(move)
                    idfs_depth.append(current_depth + 1)
                    if(self.isPuzzleSolved(new_state)):
                        self.idfs_puzzle_solved = True
                        # print(str(move))
                        self.idfsOutput += output1
                        self.idfsOutput += str(move) + "\n"
                        self.idfsOutput += self.printGameState(new_state)
                        break
            if self.idfs_puzzle_solved:
                break
        return len(self.idfs_queue) - len(idfs_stack)

    def bfs(self, i):
        # global output
        puzzle_flag = False
        nodes = 1
        while(not puzzle_flag):
            self.updateBlockDetails(self.bfs_queue[i])
            self.updateBlockDimensions()
            self.updateBlankPositions(self.bfs_queue[i])
            self.generatePossibleMoves(self.bfs_queue[i])
            # For each move generated, add the new move if not already visited
            for move in self.possible_moves.copy():
                # Updates blank positions and block with respect to current state as blank positions and block details will change
                # after applying every move
                self.updateBlockDetails(self.bfs_queue[i])
                self.updateBlockDimensions()
                self.updateBlankPositions(self.bfs_queue[i])
                new_state = self.applyMove(self.bfs_queue[i],move)
                new_state = self.normalizeState(new_state)
                if(not new_state in self.bfs_queue):
                    self.bfs_queue.append(new_state)
                    # print(str(move))
                    self.bfsOutput += str(move) + "\n"
                    #printGameState(new_state)
                    if(self.isPuzzleSolved(new_state)):
                        self.bfsOutput += self.printGameState(new_state)
                        puzzle_flag = True
                        break
            # Increment i to take next element from the queue
            i += 1
        return len(self.bfs_queue)

class BlockDetails:
    def __init__(self,count,dimen,pos):
        self.block_count = count
        self.block_dimension = dimen
        self.block_position_list = pos