import numpy as np
import matplotlib.pyplot as mtpy
import time
import os

#evaluate decision based on mode input in game setup
def opponent_ai(board,version):
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
    

def game_evaluation(board):
    win = ''
    if ():
        return True
    return False

def game(board,ai_version):
    winner = ''
    setting=ai_version
    while not game_evalution(board):
        #play game
        return 
    return -1
def main():
    board =np.arr(['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'],
                  ['*','*','*','*','*','*','*'])
    play = game(board)
    if (play.winner is not -1):
        print(f'The {play.winner} wins!')
    else:
        print('Tie!')

if __name__ == "__main__":
    main()