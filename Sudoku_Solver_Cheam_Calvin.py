import numpy as np
import matplotlib.pyplot as mtpy
import json
import time
import os

#
#Drawing heavily from https://www.geeksforgeeks.org/dsa/sudoku-backtracking-7/ for unoptimized backtracking, but tweaked to scale w 
#block size. Optimization strategies are my own code. 
#

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
    return b_end

#Main solver, times runtime and runs recursive function to compare methods
def solve_sudoku(board,size):
    sTime=time.perf_counter()
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
    slv = solve_sudoku(board,block_size)
    print("Solved Board")
    for row in slv:
        print(row)

if __name__ == "__main__":
    main()