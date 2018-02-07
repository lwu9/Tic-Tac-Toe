import os
import random
from random import randint
import numpy as np
import operator


# Need to recheck algorithm for getting all states
def createAllStates(board, player):
  won = hasWinner(board)
  global count 
  
  if won == 1 or won == -1:
    return
  else:
    for i in range(0, 9):
      if board[i] == 0:
        board[i] = player
        if board[:] not in states:
          states.append(board[:])
          V.append(determineValue(board, player))
        createAllStates(board[:], switchPlayer(player))
        board[i] = 0

def determineValue(_board, player):
  won = hasWinner(_board)
  
  # win
  if 1 == won:
    if 1 == player:
      return 1.0
    else:
      return 0.0
  # draw
  elif -1 == won:
    return 0.0
  else:
    return 0.5

def switchPlayer(player):
  if player == 1:
    return 2
  else:
    return 1

def printBoard(_board):
  size = len(_board)
  for index in range(0, size):
    if _board[index] == 1:
      print('X', end=" ")
    elif _board[index] == 2:
      print('O', end=" ")
    else:
      print('_', end=" ")
    if 0 == ((index + 1) % 3):
      print()
  
def hasWinner(_board):
  for player in range(1, 3):
    tile = tiles[player]
    
    # check horizontal
    for i in range(0, 3):
      i = i * 3
      if (_board[i]     == tile) and \
         (_board[i + 1] == tile) and \
         (_board[i + 2] == tile):
           return 1
           
    # check vertical
    for i in range(0, 3):
      if (_board[i]     == tile) and \
         (_board[i + 3] == tile) and \
         (_board[i + 6] == tile):
           return 1
           
    # check backward diagonal
    if (_board[0] == tile) and \
       (_board[4] == tile) and \
       (_board[8] == tile):
         return 1
         
    # check forward diagonal
    if (_board[6] == tile) and \
       (_board[4] == tile) and \
       (_board[2] == tile):
         return 1
  
  # check for draw
  for i in range(0, 9):
    # 0 estimated probability of winning
    if _board[i] == 0:
      return 0 
         
  # -1 is for draw match
  return -1

# each states: value
def saveStatesToFile(filename):
    fp = open(filename, "w")
    for index in range(0, len(states)):
        state_string = ':'.join(map(str,states[index]))
        value_string = str(V[index])
        fp.write("%s %s\n" %(state_string, value_string))
    fp.close()

def loadStatesFromFile(filename):
    fp = open(filename, "r")
    global totalStates
    while True:
        line = fp.readline()
        if line == "":
            break
        first_split = line.split(' ')
        state = list(map(int,first_split[0].split(':')))
        value = float(first_split[1])
        states.append(state)
        V.append(value)
        totalStates = totalStates + 1
        
def getListOfBlankTiles():
  blanks = []
  for i in range(0, 9):
    if board[i] == 0:
      blanks.append(i)
  return blanks

def greedyMove():
  maxVal = 0
  maxIndex = 0
  Vidx = []
  idx = []
  
  nextMoves = getListOfBlankTiles()

  for j in range(len(nextMoves)):
    i = nextMoves[j]
    board[i] = 1
    idx.append(states.index(board))
    board[i] = 0
    Vidx.append(V[idx[j]])

  maxVal = max(Vidx)
  maxVidxs = [i for i, j in enumerate(Vidx) if j == maxVal]
  maxVidx = random.choice(maxVidxs)
  
  maxIndex = idx[maxVidx]
  boardIndex = nextMoves[maxVidx]

  return boardIndex, maxIndex


# Just change "max" in greedyMove() into "min"
def greedyMoveOpp():
  maxVal = 0
  maxIndex = 0
  Vidx = []
  idx = []
  
  nextMoves = getListOfBlankTiles()

  for j in range(len(nextMoves)):
    i = nextMoves[j]
    board[i] = 2
    idx.append(states.index(board))
    board[i] = 0
    Vidx.append(V[idx[j]])

  maxVal = min(Vidx)
  maxVidxs = [i for i, j in enumerate(Vidx) if j == maxVal]
  maxVidx = random.choice(maxVidxs)
  
  maxIndex = idx[maxVidx]
  boardIndex = nextMoves[maxVidx]

  return boardIndex, maxIndex

# ********************Creat all possible states*******************

# board = [0,0,0,0,0,0,0,0,0]
# printBoard(board)
# player = 1
# createAllStates(board, player)
# createAllStates(board, switchPlayer(player))
# filename = "tictactoe.dat"
# totalStates = len(V)
# saveStatesToFile(filename)

# ******************** Learning Phase against Random Opponent*******************
# # step-size parameter (rate of learning)
# alpha = 0.2
# # exploration rate
# exploreRate = 0.1
# player=1
# 
# states = []
# V = []
# 
# os.chdir("/Users/lili/Documents/labproject2017/ttt")
# filename="tictactoe.dat"
# loadStatesFromFile(filename)
# states.append([0,0,0,0,0,0,0,0,0])
# V.append(0.5)
# 
# Player1Win = 0
# Player2Win = 0
# n_draw = 0
# 
# ave_reward = []
# culmutative_reward = []
# 
# n_iter = 300000
# a = n_iter / 1000
#   
# while(n_iter):
#     
#     board = [0,0,0,0,0,0,0,0,0]    
#           
#     while(True): 
#         
#         if hasWinner(board) == -1:
#             n_draw = n_draw + 1
#             break
#         
#         # Player 1
#         ex = randint(1, 100)/100.0
#         if n_iter % 1000 == 0: 
#             exploreRate = 0.1-(a-n_iter/1000)/(a-1)*0.1
#             alpha = 0.2-(a-n_iter/1000)/(a-1)*0.2
#         if ex < exploreRate:
#             nextMoves = getListOfBlankTiles()
#             userPlay = random.sample(nextMoves, k=1)
#             board[userPlay[0]] = player
#         else:
#             boardIndex, maxIndex = greedyMove()
#             tempIndex = states.index(board)
#             V[tempIndex] = V[tempIndex] + alpha*(V[maxIndex] - V[tempIndex])
#             board[boardIndex] = player             
#         #printBoard(board)
#         #print()
#         if hasWinner(board) == 1:
#             Player1Win = Player1Win + 1
#             break
#         
#         if hasWinner(board) == -1:
#             n_draw = n_draw + 1
#             break
#         
#         # Player 2
#         nextMoves = getListOfBlankTiles()
#         userPlay = random.sample(nextMoves, k=1)
#         board[userPlay[0]] = 3-player
#         #printBoard(board)
#         #print()
#         if hasWinner(board) == 1:
#             Player2Win = Player2Win + 1
#             break      
#         
#     print(n_iter, end=" ")
#     if n_iter % 100 == 0:
#         culmutative_reward.append(Player1Win)
#     n_iter = n_iter - 1
# 
# print("Player 1 # of Wins  : %d" %(Player1Win))
# print("Player 2 # of Wins  : %d" %(Player2Win))
# print("# of Draws  : %d" %(n_draw))
# filename="LearnedStateValues_300000"
# saveStatesToFile(filename)


# ****************Learning Process for the Opponent*********************
# alpha = 0.2
# # exploration rate
# exploreRate = 0.1
# player=1
# 
# states = []
# V = []
# 
# os.chdir("/Users/lili/Documents/labproject2017/ttt")
# filename="LearnedStateValues_300000"
# loadStatesFromFile(filename)
# 
# 
##Player1Win = 0
##Player2Win = 0
##n_draw = 0
##
##ave_reward = []
##culmutative_reward = []
### Take turns updating state values for player 1 and its opponent
##for i in range(10):
##    n_iter = 10000
##    a = n_iter / 1000
##    alpha = 0.2
##    # exploration rate
##    exploreRate = 0.1
##    player=1
##    while(n_iter):
##        
##        board = [0,0,0,0,0,0,0,0,0]    
##              
##        while(True): 
##            
##            if hasWinner(board) == -1:
##                n_draw = n_draw + 1
##                break
##            
##            # Player 1, take greedy action, no update
##            if n_iter % 1000 == 0: 
##                exploreRate = 0.1-(a-n_iter/1000)/(a-1)*0.1
##                alpha = 0.2-(a-n_iter/1000)/(a-1)*0.2
##            boardIndex, maxIndex = greedyMove()
##            board[boardIndex] = player             
##            #printBoard(board)
##            #print()
##            if hasWinner(board) == 1:
##                Player1Win = Player1Win + 1
##                break
##            
##            if hasWinner(board) == -1:
##                n_draw = n_draw + 1
##                break
##            
##            # Player 2, non greedy action, update its state value
##            ex = randint(1, 100)/100.0
##            if ex < exploreRate:
##                nextMoves = getListOfBlankTiles()
##                userPlay = random.sample(nextMoves, k=1)
##                board[userPlay[0]] = 3-player
##            else:
##                boardIndex, maxIndex = greedyMoveOpp()
##                tempIndex = states.index(board)
##                V[tempIndex] = V[tempIndex] + alpha*(V[maxIndex] - V[tempIndex])
##                board[boardIndex] = 3-player 
##            #printBoard(board)
##            #print()
##            if hasWinner(board) == 1:
##                Player2Win = Player2Win + 1
##                break      
##        print(n_iter, end=" ")
##        if n_iter % 100 == 0:
##            culmutative_reward.append(Player1Win)
##        n_iter = n_iter - 1
##    
##    
##    n_iter = 10000
##    a = n_iter / 1000
##    alpha = 0.2
##    # exploration rate
##    exploreRate = 0.1
##    player=1
##    while(n_iter):
##        
##        board = [0,0,0,0,0,0,0,0,0]    
##              
##        while(True): 
##            
##            if hasWinner(board) == -1:
##                n_draw = n_draw + 1
##                break
##            
##            # Player 1, non greedy action, update its state value
##            if n_iter % 1000 == 0: 
##                exploreRate = 0.1-(a-n_iter/1000)/(a-1)*0.1
##                alpha = 0.2-(a-n_iter/1000)/(a-1)*0.2
##            ex = randint(1, 100)/100.0
##            if ex < exploreRate:
##                nextMoves = getListOfBlankTiles()
##                userPlay = random.sample(nextMoves, k=1)
##                board[userPlay[0]] = player
##            else:
##                boardIndex, maxIndex = greedyMove()
##                tempIndex = states.index(board)
##                V[tempIndex] = V[tempIndex] + alpha*(V[maxIndex] - V[tempIndex])
##                board[boardIndex] = player             
##            #printBoard(board)
##            #print()
##            if hasWinner(board) == 1:
##                Player1Win = Player1Win + 1
##                break
##            
##            if hasWinner(board) == -1:
##                n_draw = n_draw + 1
##                break
##            
##            # Player 2, greedy action, no update
##            #board = flipBoard(board)
##            boardIndex, maxIndex = greedyMoveOpp()
##            board[boardIndex] = 3-player 
##            #printBoard(board)
##            #print()
##            if hasWinner(board) == 1:
##                Player2Win = Player2Win + 1
##                break      
##            #board = flipBoard(board)
##        print(n_iter, end=" ")
##        if n_iter % 100 == 0:
##            culmutative_reward.append(Player1Win)
##        n_iter = n_iter - 1
# 
# print("Player 1 # of Wins  : %d" %(Player1Win))
# print("Player 2 # of Wins  : %d" %(Player2Win))
# print("# of Draws  : %d" %(n_draw))

#*********************** Human Plays Against the Computer *********************
alpha = 0
exploreRate = 0

states = []
V = []
totalStates = 0
board = [0,0,0,0,0,0,0,0,0]
tiles = [0,1,2]
player = 1

Player1Win = 0
Player2Win = 0
n_draw = 0

#os.chdir("/Users/lili/Documents/labproject2017/ttt")
filename="Optimal_Both2"
loadStatesFromFile(filename)

while(True):
  a=input("Do you want to play first? [y/n]:")

  if a=="n":
      while(True):
              
          board = [0,0,0,0,0,0,0,0,0]    
                    
          while(True):
              if hasWinner(board) == -1:
                  n_draw = n_draw + 1
                  break
              print()
              
              boardIndex, maxIndex = greedyMove()
              tempIndex = states.index(board)
              V[tempIndex] = V[tempIndex] + alpha*(V[maxIndex] - V[tempIndex])
              board[boardIndex] = player  
              printBoard(board)
              if hasWinner(board) == 1:
                  Player1Win = Player1Win + 1
                  print("You are a loser!\n")
                  break
                  
              if hasWinner(board) == -1:
                  n_draw = n_draw + 1
                  print("A draw!\n")
                  break
                  
              
              userPlay = int(input("Enter move[1-9]: "))-1          
              board[userPlay] = 2
              printBoard(board)
              print()
              if hasWinner(board) == 1:
                  Player2Win = Player2Win + 1
                  print("You are a winner!\n")
                  break
          if input("Do you want to play again[y/n]:")!="y":
              break
  else:
      while(True):
          
          board = [0,0,0,0,0,0,0,0,0]    
                    
          while(True):
              if hasWinner(board) == -1:
                  n_draw = n_draw + 1
                  break
              print()
              
              userPlay = int(input("Enter move[1-9]: "))-1          
              board[userPlay] = 1
              printBoard(board)
              print()
              if hasWinner(board) == 1:
                  Player1Win = Player1Win + 1
                  print("You are a winner!\n")
                  break
                  
              if hasWinner(board) == -1:
                  n_draw = n_draw + 1
                  print("A draw!\n")
                  break
             
              boardIndex, maxIndex = greedyMoveOpp()
              tempIndex = states.index(board)
              V[tempIndex] = V[tempIndex] + alpha*(V[maxIndex] - V[tempIndex])
              board[boardIndex] = 3-player  
              printBoard(board)
              if hasWinner(board) == 1:
                  Player2Win = Player2Win + 1
                  print("You are a loser!\n")
                  break
          if input("Do you want to play again[y/n]:")!="y":
              break
