import random
# Will need this later when randomizing where to put the next 2.
def start_game():
    # Initialize game matrix
    mat = [[0]*4]*4
    random_two(mat)

    # Display moves available
    print("Available Moves: ")
    print("'w' : Slide Numbers Up")
    print("'s' : Slide Numbers Down")
    print("'a' : Slide Numbers Left")
    print("'d' : Slide Numbers Right")
    return mat

# Inserts a random two into any space with 0
def random_two(mat):
    # Find an empty space by searching random cells 40 times
    searches = 0
    while searches < 40:
        row = random.randint(0,3)
        cell = random.randint(0,3)
        if mat[row][cell] == 0:
            mat[row][cell] = 2
            return
        searches += 1
    
    # If the random search 40 times does not find an empty space, find one manually
    for i in range(0,3):
        for j in range(0,3):
            if mat[i][j] == 0:
                mat[i][j] = 2
    return

# Determines the current state of the game.
def game_state(mat):
    # There are 4 cases to consider: 
    # Case 1: The game has a 2048, so you win.
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 2048:
                return 'YOU WON'
    
    # Case 2: There are available spaces, so the game is not over.
    for i in range(4):
        for j in range(4):
            if mat[i][j]== 0:
                return 'GAME ONGOING'

    # Case 3: There are no available spaces but there are available moves. 
    # To find this, just see if any cells have the same value as the space to the right or below it.
    # This first nested loop checks the upper left 3x3 spaces.
    for i in range(3):
        for j in range(3):
            if mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1]:
                return 'GAME ONGOING'
            
    # This loop checks the bottom row if a cell is equal to the cell beside it. 
    for i in range(3):
        if mat[3][i] == mat[3][i+1]:
            return 'GAME ONGOING'
        
    # This loop checks the rightmost column if a cell is equal to the cell under it. 
    for i in range(3):
        if mat[i][3] == mat[i+1][3]:
            return 'GAME ONGOING'

    # Case 4: There are no available spaces and no available moves, so you lose.
    return 'YOU LOST'

# Slides all numbers compressed along the left edge.
# Intuition is that you go through each cell and if it isn't 0, set pos cell to that value, then set the original cell to 0.
# Then, add 1 to pos since you will now slide next non-zero value to that cell.
def slide_sideways(mat):
    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                x = mat[i][j]
                mat[i][j] = 0
                mat[i][pos] = x
                pos += 1
    return mat

# Adds pairs of numbers starting from the left. Sum is left term and leaves right term as 0.
# Combining add_sideways and slide_sideways will give us our move_left and move_right functions.
def add_sideways(mat):
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j+1]:
                mat[i][j] *= 2
                mat[i][j+1] = 0
    return mat

# Will need this function to differentiate left-right and up-down moves.
def reverse_rows(mat):
    for row in mat:
        row.reverse()
    return mat

# Slide to the left, then add, then slide to the left again.
# Not calling random_two here because I use this function in move_right.
def move_left(mat):
    slide_sideways(mat)
    add_sideways(mat)
    slide_sideways(mat)
    return mat

# Sliding to the right is equivalent to reversing, then slide left, then reverse again.
# Not calling random_two here because I want to keep consistency in my move_left and move_right function.
def move_right(mat):
    reverse_rows(mat)
    move_left(mat)
    reverse_rows(mat)
    return mat

# I could make completely new functions for the move_up and move_down functions, instead I will create a transpose_matrix
# function. This function will convert rows into columns and columns into rows, which I can then use in addition to 
# move_left and move_right to move_up and move_down
def transpose_matrix(mat):
    transposed = []
    for i in range(4):
        new_row =[]
        for j in range(4):
            new_row.append(mat[j][i])
        transposed.append(new_row)
    mat = transposed
    return mat

# Transposing converts the top row into the leftmost column. 
# Therefore, moving up is related to moving the transposed matrix left  and transposing it again.
def move_up(mat):
    mat = transpose_matrix(mat)
    mat = move_left(mat)
    mat = transpose_matrix(mat)
    return mat

# Moving down is related to moving the transposed matrix right and transposing it again.
def move_down(mat):
    mat = transpose_matrix(mat)
    mat = move_right(mat)
    mat = transpose_matrix(mat)
    return mat
