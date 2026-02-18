import numpy as np
import matplotlib.pyplot as mtpy


#AI decision makers
def AB_choice(board,side):
    return -1
def MCTS_choice(board,side):
    return -1
#evaluate decision based on mode input in game setup
def ai_choice(board,version,side):
    choice = 0
    columns = np.array([0,1,2,3,4,5,6])
    if version is 'AB':
        choice =1
    elif version is 'MCTS':
        choice =1
    elif version is 'dumb':
        choice = np.random.choice(columns)
    else:
        return choice
    

def game_evaluation(board,player):
    rows,cols = board.shape
    #horizontal and vertial check
    for r in range(rows):
        for c in range(cols-3):
            if all(board[r,c+i] == player for i in range(4)):
                return True
    for r in range(rows-3):
        for c in range(cols):
            if all(board[r+i,c] == player for i in range(4)):
                return True
    #diagonal checks
    for r in range(3,rows):
        for c in range(cols-3):
            if all(board[r-i,c+i] == player for i in range(4)):
                return True
    for r in range(rows-3):
        for c in range(cols-3):
            if all(board[r+i,c+i] == player for i in range(4)):
                return True
    return False

def update_board(board,col_choice):
    board_cp=board[:]
    board_update = False
    while not board_update:
        for row in range(col_choice):
            board_update=True
    return board_cp

def game(board,ai_version,player):
    winner = ''
    AI_W='AI'
    P_W='Player'
    player1='O'
    player2='0'
    play_board=board[:]
    victory=False
    #sanitize inputs to ensure program runs
    if ai_version is 'AB' or 'MCTS' or 'dumb':
        setting=ai_version
    else: 
        setting='dumb'
    if player is 'Y':
        play=player
    else:
        play='N'
    #main game loop
    while not victory:
        #play game
        if play is not 'N':
            #player loop
            victory=game_evaluation(play_board,player1)
        else:
            #autorun using set data
            victory=game_evaluation(play_board,player1)
    return -1

def main():
    board =np.arr(['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'])
    OS=input('Select AI version (AB version, MCTS version, or dumb)(default is dumb):')
    real_player=input('Player or AI opponent? (Y/N)(default is AI)')
    play = game(board,OS,real_player)
    if (play.winner is not -1):
        print(f'The {play.winner} wins!')
    else:
        print('Tie!')

if __name__ == "__main__":
    main()