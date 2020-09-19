import tetrisBoard
import time
import random

def playTetris(canvas):
    board = tetrisBoard.Board(16, 10)
    board.makeNewPiece()
    
    while (board.gameStep()):
        time.sleep(0.5)
        canvas.tetris2pixel_array(board.getBoard())
        canvas.display()
        board.makeMove(board.chooseOkMove())
    
    time.sleep(0.5)
    canvas.tetris2pixel_array(board.getBoard())
    canvas.blink()