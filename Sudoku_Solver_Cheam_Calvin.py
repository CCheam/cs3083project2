import numpy as np
import matplotlib.pyplot as mtpy
import json
import time
import os

#
#Drawing heavily from https://www.geeksforgeeks.org/dsa/sudoku-backtracking-7/ for unoptimized backtracking, but tweaked to scale w 
#block size. Optimization strategies are my own code. 
#

#checks if a number will work in a square
def valid_sq_check(board,row,col,num,block_size):

    #check by row, set to be col for scalability
    for x in range(col):
        if(board[row][x] == num):
            return False
    #check by row, set to be col for scalability
    for x in range(row):
        if(board[x][col] == num):
            return False
        
    #loop through square
    sRow = row - (row % block_size)
    sCol = col - (col % block_size)

    for i in range(block_size):
        for j in range(block_size):
            if(board[sRow+i][sCol+j] == num):
                return False
    return True

#master func to use random or MRV to pick next cell
def select_variable_CS(board,b_size,MRV):
    board_size=b_size*b_size
    #2 choice funcs, randomly from empty sqs and other w least possible options
    def rand_selec():
        empty_sqs=[]
        for row in board_size:
            for col in board_size:
                if board[row][col]==0:
                    empty_sqs.append(board[row][col])
        if not empty_sqs: 
            return None
        #random choice from empty sqs
        pick=np.random.choice(len(empty_sqs))
        return empty_sqs[pick] 
    def MRV_selec():
        max_col=board_size + 1
        choice=None
        for row in board_size:
            for col in board_size:
                if board[row][col]==0:
                    #loops through all possible nums, returns the pos w smallest number of potential choices
                    count = 0
                    for num in range(1, max_col + 1):
                        if valid_sq_check(board, row, col, num, b_size):
                            count += 1
                    if count < max_col:
                        max_col=count
                        choice = (row,col)
        return choice
    if MRV:
        return MRV_selec()
    else:
        return rand_selec()

#master func to return ordered possible values for each sq
def order_values(board,row,col,b_size,ODV_switch):
    b_end=b_size*b_size
    def standard():
        return [num for num in range(1, b_end + 1)
                if valid_sq_check(board, row, col, num, b_size)]
    def LCV():
        def constraint_check(num):
            constraints=0
            for c in range(b_end):                    # check by row
                if board[row][c] == 0 and c != col:
                    if not valid_sq_check(board, row, c, num, b_size):
                        constraints += 1
            for r in range(b_end):                    # check by col
                if board[r][col] == 0 and r != row:
                    if not valid_sq_check(board, r, col, num, b_size):
                        constraints += 1
            bRow = row - (row % b_size)               # check by block
            bCol = col - (col % b_size)
            for i in range(b_size):
                for j in range(b_size):
                    r, c = bRow + i, bCol + j
                    if board[r][c] == 0 and (r, c) != (row, col):
                        if not valid_sq_check(board, r, c, num, b_size):
                            constraints += 1
            return constraints
        valid_sqs=[]
        return sorted(valid_sqs,key=constraint_check)
    if ODV_switch:
        return LCV()
    else:
        return standard()
    return None
#master recursion function
def infer_new_steps(board,row,col,b_size,INFR):
    b_end = b_size * b_size
    value=[]
    return value
#unoptimized solver    
def sudoku_solved_uo(board,row,col,b_size):
    b_end = b_size * b_size
    #end looping at end of rows
    if row == (b_end -1) and col == (b_end):
        return board
    #col looping
    if col == b_end:
        row+=1
        col=0
    #pass over occupied sqs
    if board[row][col] != 0:
        return(sudoku_solved_uo(board,row,col+1,b_size))

    for num in range(1,b_end+1):
        if (valid_sq_check(board,row,col,num,b_size)):
            board[row][col]=num
            r = sudoku_solved_uo(board,row,col+1,b_size)
            if r:
                return r
            board[row][col]=0
            
    return None
    
#optimized solver, takes bools to turn functions on
def sudoku_solved_mxo(board, row, col, b_size, MRV, INFR, ODV):
    b_end = b_size * b_size
    #utilize MRV/random to pick next open cell, sequential check only last fallback
    cell = select_variable_CS(board, b_size,MRV)
    # Unoptimized linear search for if next cell selector absolutely fails
    if cell is None:
        if row == b_end:
            return board
        if col == b_end:
            return sudoku_solved_mxo(board, row + 1, 0, b_size, MRV, INFR, ODV)
        if board[row][col] != 0:
            return sudoku_solved_mxo(board, row, col + 1, b_size, MRV, INFR, ODV)
        cell = (row, col)                         
    row, col = cell

    # gather remaining sqs
    leftovers = order_values(board,row,col,b_size,ODV)
    #main recursion loop
    for num in leftovers:
        board[row][col] = num
        # recursion choices
        infer_new_steps()
        board[row][col] = 0

    return None

#Main solver, times runtime and runs recursive function. Checks if settings is not none to run
def solve_sudoku(board,size,settings):
    sTime=time.perf_counter()
    if settings is not None:
        s = sudoku_solved_mxo(board,0,0,size,settings)
    else:
        s = sudoku_solved_uo(board,0,0,size)
    eTime=time.perf_counter()
    rTime=eTime-sTime
    print(f"Time to run: {rTime:.6f} seconds")
    return s 


def main():
    block_size = 3
    empty_sqs = 30
    block_size_sq = block_size * block_size
    block_file= f"sudoku{block_size_sq}.json"
    #dynamically run sudoku generator based off of passed in vars
    os.system(f"python SudokuGenerator.py {empty_sqs} --output_file {block_file} --block_size {block_size}")
    with open(block_file, "r") as f:
        board = json.load(f)
    # print solved/unsolved
    print("Unsolved Board")
    for row in board:
        print(row)
    slv = solve_sudoku(board,block_size,False,False,False)
    print("Solved Board")
    for row in slv:
        print(row)


if __name__ == "__main__":
    main()