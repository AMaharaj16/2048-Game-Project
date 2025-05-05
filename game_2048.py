import logic_2048

if __name__ == '__main__':
    mat = logic_2048.start_game()
    logic_2048.print_mat(mat)

state = 'GAME ONGOING'

while state == 'GAME ONGOING':
    move = input("Next Move:")
    if move == 'w':
        mat = logic_2048.move_up(mat)
        mat = logic_2048.random_two(mat)
    
    if move == 's':
        mat = logic_2048.move_down(mat)
        mat = logic_2048.random_two(mat)
    
    if move == 'a':
        mat = logic_2048.move_left(mat)
        mat = logic_2048.random_two(mat)

    if move == 'd':
        mat = logic_2048.move_right(mat)
        mat = logic_2048.random_two(mat)

    state = logic_2048.game_state(mat)
    logic_2048.print_mat(mat)
    print(state)