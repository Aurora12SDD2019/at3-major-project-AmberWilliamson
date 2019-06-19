""" Developed on python 3.7 using pygame 1.9.6 for SDD yr12 course
"""

__author__ = "Amber Williamson"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "amber.williamson@education.nsw.com.au"
__status__ = "Alpha"

#dependencies
import random
import mods
import copy
import sys
import pygame
from pygame.locals import *

SCREENWIDTH = 7  
SCREENHEIGHT = 6 
assert SCREENWIDTH >= 4 and SCREENHEIGHT >= 4

DIFFICULTY = 1 #how many moves ahead the AI will look before dtermining it's move, 0-2 only or the game will not run

SPACESIZE = 50 

FPS = 60
WINDOWWIDTH = 640 
WINDOWHEIGHT = 480

XMARGIN = int((WINDOWWIDTH - SCREENWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - SCREENHEIGHT * SPACESIZE) / 2)

BLUE = (5, 0, 165)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BGCOLOUR = BLUE
TEXTCOLOUR = WHITE

RED = 'red'
YELLOW = 'yellow'
EMPTY = None
PLAYER = 'player'
CPU = 'cpu'


def main():
    global CLOCK, DISPLAY, REDPILERECT, YELLOWPILERECT, REDTOKENIMG
    global YELLOWTOKENIMG, BOARDIMG, HELPIMG, HELPRECT, PLAYERWINNERIMG
    global CPUWINNERIMG, WINNERRECT, DRAWWINNERIMG

    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Connect 4')
    background_muzak = pygame.mixer.Sound('sound/do_do_do.ogg')

    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    YELLOWPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    REDTOKENIMG = pygame.image.load('red_token.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    YELLOWTOKENIMG = pygame.image.load('yellow_token.png')
    YELLOWTOKENIMG = pygame.transform.smoothscale(YELLOWTOKENIMG, (SPACESIZE, SPACESIZE))
    BOARDIMG = pygame.image.load('the_board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))
    PLAYERWINNERIMG = pygame.image.load('player_winner.png')
    CPUWINNERIMG = pygame.image.load('cpu_winner.png')
    DRAWWINNERIMG = pygame.image.load('draw_tie.png')
    WINNERRECT = PLAYERWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    HELPIMG = pygame.image.load('tutorial_help.png')
    HELPRECT = HELPIMG.get_rect()
    HELPRECT.left = REDPILERECT.right + 10
    HELPRECT.centery = REDPILERECT.centery

    isFirstGame = True

    while True:
        background_muzak.play()
        runGame(isFirstGame)
        isFirstGame = False


def runGame(isFirstGame):
    if isFirstGame:
        turn = CPU
        showHelp = True
    else:
        if random.randint(0, 1) == 0:
            turn = CPU
        else:
            turn = PLAYER
        showHelp = False

    mainBoard = getNewBoard()

    while True: 
        if turn == PLAYER:
            getPlayerMove(mainBoard, showHelp)
            if showHelp:
                showHelp = False
            if isWinner(mainBoard, RED):
                winnerImg = PLAYERWINNERIMG
                break
            turn = CPU
        else:
            column = getCPUMove(mainBoard)
            animateCPUMoving(mainBoard, column)
            makeMove(mainBoard, YELLOW, column)
            if isWinner(mainBoard, YELLOW):
                winnerImg = CPUWINNERIMG
                break
            turn = PLAYER

        if isBoardFull(mainBoard):
            winnerImg = DRAWWINNERIMG
            break

    while True:
        drawBoard(mainBoard)
        DISPLAY.blit(winnerImg, WINNERRECT)
        pygame.display.update()
        CLOCK.tick()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == Q_ESCAPE):
                print('Thanks for playing!')
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def makeMove(board, player, column):
    lowest = getLowestEmptySpace(board, column)
    if lowest != -1:
        board[column][lowest] = player


def drawBoard(board, extraToken=None):
    DISPLAY.fill(BGCOLOUR)

    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(SCREENWIDTH):
        for y in range(SCREENHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == RED:
                DISPLAY.blit(REDTOKENIMG, spaceRect)
            elif board[x][y] == YELLOW:
                DISPLAY.blit(YELLOWTOKENIMG, spaceRect)

    if extraToken != None:
        if extraToken['colour'] == RED:
            DISPLAY.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['colour'] == YELLOW:
            DISPLAY.blit(YELLOWTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    for x in range(SCREENWIDTH):
        for y in range(SCREENHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            DISPLAY.blit(BOARDIMG, spaceRect)

    DISPLAY.blit(REDTOKENIMG, REDPILERECT)
    DISPLAY.blit(YELLOWTOKENIMG, YELLOWPILERECT)


def getNewBoard():
    board = []
    for x in range(SCREENWIDTH):
        board.append([EMPTY] * SCREENHEIGHT)
    return board


def getPlayerMove(board, isFirstMove):
    draggingToken = False
    tokenx, tokeny = None, None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
                draggingToken = True
                tokenx, tokeny = event.pos
            elif event.type == MOUSEMOTION and draggingToken:
                tokenx, tokeny = event.pos
            elif event.type == MOUSEBUTTONUP and draggingToken:
                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:
                    column = int((tokenx - XMARGIN) / SPACESIZE)
                    if isValidMove(board, column):
                        animateDroppingToken(board, column, RED)
                        board[column][getLowestEmptySpace(board, column)] = RED
                        drawBoard(board)
                        pygame.display.update()
                        return
                tokenx, tokeny = None, None
                draggingToken = False
        if tokenx != None and tokeny != None:
            drawBoard(board, {'x':tokenx - int(SPACESIZE / 2), 'y':tokeny - int(SPACESIZE / 2), 'colour':RED})
        else:
            drawBoard(board)

        if isFirstMove:
            DISPLAY.blit(HELPIMG, HELPRECT)

        pygame.display.update()
        CLOCK.tick()


def animateDroppingToken(board, column, colour):
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE
    dropSpeed = 1.0

    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            return
        drawBoard(board, {'x':x, 'y':y, 'colour':colour})
        pygame.display.update()
        CLOCK.tick()


def animateCPUMoving(board, column):
    x = YELLOWPILERECT.left
    y = YELLOWPILERECT.top
    speed = 1.0
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'colour':YELLOW})
        pygame.display.update()
        CLOCK.tick()
    y = YMARGIN - SPACESIZE
    speed = 1.0
    while x > (XMARGIN + column * SPACESIZE):
        x -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'colour':YELLOW})
        pygame.display.update()
        CLOCK.tick()
    animateDroppingToken(board, column, YELLOW)


def getCPUMove(board):
    potentialMoves = getPotentialMoves(board, YELLOW, DIFFICULTY)
    bestMoveFitness = -1
    for i in range(SCREENWIDTH):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i)
    return random.choice(bestMoves)


def getPotentialMoves(board, tile, lookAhead):
    if lookAhead == 0 or isBoardFull(board):
        return [0] * SCREENWIDTH

    if tile == RED:
        CPUTile = YELLOW
    else:
        CPUTile = RED

    potentialMoves = [0] * SCREENWIDTH
    for firstMove in range(SCREENWIDTH):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, firstMove):
            continue
        makeMove(dupeBoard, tile, firstMove)
        if isWinner(dupeBoard, tile):
            potentialMoves[firstMove] = 1
            break 
        else:
            if isBoardFull(dupeBoard):
                potentialMoves[firstMove] = 0
            else:
                for counterMove in range(SCREENWIDTH):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, counterMove):
                        continue
                    makeMove(dupeBoard2, CPUTile, counterMove)
                    if isWinner(dupeBoard2, CPUTile):
                        potentialMoves[firstMove] = -1
                        break
                    else:
                        results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / SCREENWIDTH) / SCREENWIDTH
    return potentialMoves


def getLowestEmptySpace(board, column):
    for y in range(SCREENHEIGHT-1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def isValidMove(board, column):
    if column < 0 or column >= (SCREENWIDTH) or board[column][0] != EMPTY:
        return False
    return True


def isBoardFull(board):
    for x in range(SCREENWIDTH):
        for y in range(SCREENHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


def isWinner(board, tile):
    for x in range(SCREENWIDTH - 3):
        for y in range(SCREENHEIGHT):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    for x in range(SCREENWIDTH):
        for y in range(SCREENHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    for x in range(SCREENWIDTH - 3):
        for y in range(3, SCREENHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True
    for x in range(SCREENWIDTH - 3):
        for y in range(SCREENHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False


if __name__ == '__main__':
    main()
