import tetrisBoard
import time
import random

newboard = tetrisBoard.Board(16, 10)

newboard.active_piece = tetrisBoard.Piece(tetrisBoard.YELLOW, [15,4])
#newboard.board_array[13] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#newboard.board_array[14] = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
#newboard.board_array[15] = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1]


newboard.printBoard()
time.sleep(0.5)

while (newboard.gameStep()):
    time.sleep(0.5)
    newboard.printBoard()
    newboard.makeMove(random.randrange(3))
    
time.sleep(0.5)
newboard.printBoard()



print("Game Over!")
