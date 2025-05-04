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
