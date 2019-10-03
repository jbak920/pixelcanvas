from __future__ import print_function
import numpy
from random import randint
import os
import sys
from utils import Color
import copy

BLANK  = Color(000, 000, 000) # empty space
CYAN   = Color(000, 255, 255) #long piece
BLUE   = Color(000, 000, 255) #backwards L
ORANGE = Color(255, 165, 000) #normal L
YELLOW = Color(255, 255, 000) #square
GREEN  = Color(000, 128, 000) #backwards z
PURPLE = Color(128, 000, 128) #t
RED    = Color(255, 000, 000) #normal z

COLORS = [BLANK, CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

MOVLEFT = 0
MOVRIGHT = 1
POSROT = 2 # Counter-clockwise
NEGROT = 3 # Clockwise

class Piece:
    '''Tetris has 7 pieces'''
    def __init__(self, color, origin):
        self.color = color
        self.origin = origin
        self.setSquares(color)
        self.orientation = UP
        
        
    def setSquares(self, color):
        # squares is 2x4 array with relative positions of squares for the piece
        # indexing is [y,x] or [row, col] relative to origin.
        # See tetris wiki for origin locations, with the exception of
        # the I piece because I am lazy.
        self.squares = [[0,0]] 
        if(color == BLANK):
            self.squares = [[]]
        if(color == CYAN): #long piece (or I)
            self.squares.append([0,1])
            self.squares.append([0,-1])
            self.squares.append([0,2])
        elif(color == BLUE): # backwards L (or J)
            self.squares.append([0,1])
            self.squares.append([0,-1])
            self.squares.append([1,-1])
        elif(color == ORANGE): # normal L
            self.squares.append([0,1])
            self.squares.append([0,-1])
            self.squares.append([1,1])
        elif(color == YELLOW): # square (or O)
            self.squares.append([0,1])
            self.squares.append([1,0])
            self.squares.append([1,1])
        elif(color == GREEN): # backwards z (or S)
            self.squares.append([0,-1])
            self.squares.append([1,0])
            self.squares.append([1,1])
        elif(color == PURPLE): # T shape
            self.squares.append([0,-1])
            self.squares.append([1,0])
            self.squares.append([0,1])
        elif(color == RED): # normal z
            self.squares.append([0,1])
            self.squares.append([1,0])
            self.squares.append([1,-1])
        

class Board:
    '''This is the state of the tetris board'''

    def __init__(self, display_height, width):
        '''Initialize with display height, not true height.'''
        self.DISPLAY_HEIGHT = display_height
        self.TRUE_HEIGHT = display_height + 2 #2 rows exist above the top of the screen
        self.WIDTH = width
        self.active_piece = None
        self.board_array = []
        # Build up the 2d squares list element-by-element
        # index by [row][col], or [y][x], with [0][0] being bottom-left.
        for row in range(self.TRUE_HEIGHT):
            self.board_array.append([])
            for col in range(self.WIDTH):
                self.board_array[row].append(0)

    def setVal(self, row, col , val):
        '''Sets a value in the squares array'''
        self.board_array[row][col] = val


    def printBoard(self):
        '''Prints the board to stdout; empty squares are left blank'''
        #First, put the active piece into the board temporarily
        os.system('clear')
        need_to_take_off = False
        if (self.checkValidPiecePosition() == True and self.active_piece.color != BLANK and self.checkCollision() == False):
            need_to_take_off = True
            self.putPieceOnBoard()
        else:
            print("The piece is not in a valid position for displaying!")
        for row in reversed(range(self.DISPLAY_HEIGHT)): # print from the top-down
            print("+", sep='', end='')
            for col in range(self.WIDTH):
                print("---+", sep='', end='')
            print("")
            for col in range(self.WIDTH):
                # check if square is empty
                if(self.board_array[row][col] != 0 ):
                    print("| " + str(self.board_array[row][col]) + " ", sep='', end='')
                else:
                    print("|   ", sep='', end='')
            print("|"),
        print("+", sep='', end='')
        for col in range(self.WIDTH):
            print("---+", sep='', end='')
        print("")
        #Take the piece off the board, but only if it was put on in the first place
        if (need_to_take_off == True):
            self.takePieceOffBoard()

    def getBoard(self):
        '''Gets the full board array, including the active piece, but NOT including extra rows'''
        #First, put the active piece on temporarily
        need_to_take_off = False
        if (self.checkValidPiecePosition() == True and self.active_piece.color != BLANK and self.checkCollision() == False):
            need_to_take_off = True
            self.putPieceOnBoard()
	else:
	    print("The piece is not in a valid position for displaying!")
        retArray = copy.deepcopy(self.board_array)

        # Pop last two items off the top
        retArray.pop()
        retArray.pop()

        #Take the piece off the board, but only if it was put on in the first place
        if (need_to_take_off == True):
            self.takePieceOffBoard()

        return retArray

    def putPieceOnBoard(self):
        '''Places the active piece onto the board. If the piece overlaps
           with nonzero entries in the board, the board will be overwritten.'''
        if(self.active_piece != None):
            for square in self.active_piece.squares:
                row = self.active_piece.origin[0] + square[0]
                col = self.active_piece.origin[1] + square[1]
                self.board_array[row][col] = self.active_piece.color

    def takePieceOffBoard(self):
        '''Removes the active pieces from the board, replacing the squares with BLANK.'''
        if(self.active_piece != None):
            for square in self.active_piece.squares:
                row = self.active_piece.origin[0] + square[0]
                col = self.active_piece.origin[1] + square[1]
                self.board_array[row][col] = BLANK

    def checkValidPiecePosition(self):
        '''Checks only if the piece exists within the board limits,
           not if the piece is colliding with existing squares.'''
        valid = True
        if(self.active_piece.color != BLANK):
            for square in self.active_piece.squares:
                row = self.active_piece.origin[0] + square[0]
                col = self.active_piece.origin[1] + square[1]
                if (row < 0 or row >= self.TRUE_HEIGHT):
                    valid = False
                    break
                if (col < 0 or col >= self.WIDTH):
                    valid = False
                    break
        return valid
        
    def checkCollision(self):
        '''Checks for collision between the active piece and any static squares
           currently on the board. Return True if there is a collision, False if not.'''

        collision = False
        for square in self.active_piece.squares:
            row = self.active_piece.origin[0] + square[0]
            col = self.active_piece.origin[1] + square[1]
            if (row < 0):
                collision = True
                break
            elif (self.board_array[row][col] != 0):
                collision = True
                break
        return collision
                
    def tickDown(self):
        '''Tries to move the active piece down by 1 tick. If it can, it does. If it can't,
           either because it would cause collision with the bottom of the board or existing pieces,
           leave the piece unchanged.

           Return True on success, False on fail.'''
        success = True
        if (self.checkValidPiecePosition() == True):
            self.active_piece.origin[0] -= 1
            if (self.checkValidPiecePosition() == False):
                self.active_piece.origin[0] += 1
                success = False
            elif (self.checkCollision() == True):
                self.active_piece.origin[0] += 1
                success = False
        else:
            print("Invalid position detected!")
        return success

    def makeNewPiece(self):
        '''Randomly chooses a new piece and puts it in just above the visible board.
           Then ticks down once - if this fails, it means a game over. Therefore this
           function returns False if a gameover state is detected.'''
        temp_rand = randint(1,7)
        newcolor = COLORS[temp_rand]
        neworigin = [self.DISPLAY_HEIGHT, (self.WIDTH-1)/2]
        self.active_piece = Piece(newcolor, neworigin)
        return self.tickDown()

    def gameStep(self):
        '''Ticks the active piece down once; if it fails, glue the piece down and make a new piece.
           
           Returns True on success, False on game over detected.'''
        success = True
        if(self.checkValidPiecePosition() == True):
            if(self.tickDown() == False):
                self.putPieceOnBoard()
                self.clearLines()
                success = self.makeNewPiece()
        else:
            success = False
            print("Invalid location detected!")
        return success
        
    def makeMove(self, move):
        '''Either moves the piece left or right, or makes a rotation.
           If the move is invalid, the move does not occur. No wall kicks.'''
        if(move == MOVLEFT):
            self.active_piece.origin[1] -= 1
            if(self.checkValidPiecePosition() == False):
                self.active_piece.origin[1] += 1
            elif(self.checkCollision() == True):
                self.active_piece.origin[1] += 1
        elif(move == MOVRIGHT):
            self.active_piece.origin[1] += 1
            if(self.checkValidPiecePosition() == False):
                self.active_piece.origin[1] -= 1
            elif(self.checkCollision() == True):
                self.active_piece.origin[1] -= 1
        elif(move == POSROT):
            self.makePositiveRotation()
            if(self.checkValidPiecePosition() == False):
                self.makeNegativeRotation()
            elif(self.checkCollision() == True):
                self.makeNegativeRotation()
        elif(move == NEGROT):
            self.makeNegativeRotation()
            if(self.checkValidPiecePosition() == False):
                self.makePositiveRotation()
            elif(self.checkCollision() == True):
                self.makePositiveRotation()
           
    def makePositiveRotation(self):
        # For a 90-degree CCW rotation:
        # x -> -y
        # y -> x
        for square in self.active_piece.squares:
            tempx = square[1]
            tempy = square[0]
            square[1] = -tempy
            square[0] = tempx
        
    def makeNegativeRotation(self):
        # For a 90-degree CCW rotation:
        # x -> y
        # y -> -x
        for square in self.active_piece.squares:
            tempx = square[1]
            tempy = square[0]
            square[1] = tempy
            square[0] = -tempx

    def checkRow(self, whole_row):
        '''Checks if a row is full and needs to be cleared.
           Returns True if it needs to be cleared.'''
        full_state = True
        for col in whole_row:
            if (col == 0):
                full_state = False
                break
        return full_state
        
    def clearLines(self):
        '''Clears all full rows from the board.'''
        rows_to_pop = []
        for row in self.board_array:
            if (self.checkRow(row) == True):
                rows_to_pop.append(row)
        for row in rows_to_pop:
            self.board_array.remove(row)
            self.board_array.append([])
            for col in range(self.WIDTH):
                self.board_array[self.TRUE_HEIGHT-1].append(0)
                    



