""" Short, one line description of the project ending with a period.
A longer description of the module with details that may help the user or anybody
reviewing the code later. make sure you outline in detail what the module does and how it can be used.
"""

__author__ = "Amber Williamson"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "amber.williamson@education.nsw.com.au"
__status__ = "Alpha"


""" revision notes:


"""

#import statements for any dependencies


#modules - write your modules here using the templates below


# templates
def runGame(isFirstGame):
    if isFirstGame:
        turn = COMPUTER
        showHelp = True
    else:
        if random.randint(0, 1) == 0:
            turn = COMPUTER
        else:
            turn = HUMAN
        showHelp = False

    mainBoard = getNewBoard()
    
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


def getHumanMove(board, isFirstMove):
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


def animateComputerMoving(board, column):
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


def getComputerMove(board):
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
        enemyTile = YELLOW
    else:
        enemyTile = RED

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
                    makeMove(dupeBoard2, enemyTile, counterMove)
                    if isWinner(dupeBoard2, enemyTile):
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

        
        
    """Does something amazing.

    a much longer description of the really amazing stuff this function does and how it does it.

    Args:
        arg1: the first argument required by the function.
        arg2: the second argument required by the function.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        description of the stuff that is returned by the function.

    Raises:
        AnError: An error occurred running this function.
    """
    pass



class SampleClass(object):
    """Summary of class here.

    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

   