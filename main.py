#Draw Board
from cmu_graphics import *
from flashLight import *
from darkMode import *
from BSPTreeSetup import *
from drawPacManPlayer import * 
import random






def onAppStart(app):
    PacManOnAppStart(app)
    #best record(DO NOT add to reset app)
    app.bestRecordTime = None
    app.bestRecordTreasure = None
    #timer
    app.stepsPerSecond = 50
    app.stepsTaken = 0
    app.seconds = 120
    app.secondsElapsed = 0
    #game mode
    app.gameOver = False
    app.darkMode = True
    #board info
    app.rows = 20
    app.cols = 20
    app.boardLeft = 100
    app.boardTop = 75
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 0.5
    app.width = 600
    app.height = 600
    #rooms and tile categorizing
    app.curRoomLength = 12
    app.board = [[None for i in range(app.cols)]for j in range (app.rows)]
    app.roomTreeRoot = splitDungeon(app, 0, 0, app.cols, app.rows, 0, 8)
    app.wallPositions = set()
    app.floorPositions = set()
    app.treasurePosition = set()
    app.showWall = set()
    app.showTreasure = set()
    app.polygonPoints = []
    app.treasureLeft = 5
    connectRooms(app, app.roomTreeRoot)
    #categorize the tiles to make collision check easier
    for row in range(app.rows):
        for col in range(app.cols):
            if (row, col) in app.floorPositions:
                app.board[row][col] = 'floor'
            elif (row, col) in app.wallPositions:
                app.board[row][col] = 'wall'
            else:
                app.board[row][col] = None
    onAppStartHelper(app)
    placeTreasure(app)
    #find a random floor tile to start the player on
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 'floor':
                cellWidth, cellHeight = getCellSize(app)
                app.cx = app.boardLeft + col * cellWidth + cellWidth // 2
                app.cy = app.boardTop + row * cellHeight + cellHeight // 2
                break
    
def restApp(app):
    app.secondsElapsed = 0
    app.stepsPerSecond = 50
    app.stepsTaken = 0
    app.seconds = 120
    app.gameOver = False
    app.darkMode = True
    app.rows = 20
    app.cols = 20
    app.boardLeft = 100
    app.boardTop = 75
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 0.5
    app.width = 600
    app.height = 600
    app.curRoomLength = 12
    app.board = [[None for i in range(app.cols)]for j in range (app.rows)]
    app.roomTreeRoot = splitDungeon(app, 0, 0, app.cols, app.rows, 0, 8)
    app.wallPositions = set()
    app.floorPositions = set()
    app.treasurePosition = set()
    app.showWall = set()
    app.showTreasure = set()
    app.polygonPoints = []
    app.treasureLeft = 5
    connectRooms(app, app.roomTreeRoot)
    #categorize the tiles to make collision check easier
    for row in range(app.rows):
        for col in range(app.cols):
            if (row, col) in app.floorPositions:
                app.board[row][col] = 'floor'
            elif (row, col) in app.wallPositions:
                app.board[row][col] = 'wall'
            else:
                app.board[row][col] = None
    onAppStartHelper(app)
    placeTreasure(app)
    #find a random floor tile to start the player on
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 'floor':
                cellWidth, cellHeight = getCellSize(app)
                app.cx = app.boardLeft + col * cellWidth + cellWidth // 2
                app.cy = app.boardTop + row * cellHeight + cellHeight // 2
                break


#start screen ################
def start_redrawAll(app):
    drawLabel('Welcome', app.width//2, app.height//2, size = 24, bold = True)
    drawLabel('press space to begin!', app.width//2, app.height//2+40, size = 16) 
    if app.bestRecordTime!= None and app.bestRecordTreasure !=None:
        bestMinute = app.bestRecordTime // 60
        bestSecond = app.bestRecordTime%60
        drawLabel(f'Your best record is {app.bestRecordTreasure} treasures found in {bestMinute}min{bestSecond}sec!', app.width//2, app.height//2+80, size = 16, bold = True)
    elif app.bestRecordTime == None and app.bestRecordTreasure == None:
        drawLabel(f'No records yet! Start playing to set a record', app.width//2, app.height//2+80, size = 16, bold = True)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')   

#end screen ################
def end_redrawAll(app):
    drawLabel('Game Ended!', app.width//2, app.height//2-40, size = 24, bold = True)
    minute = app.secondsElapsed // 60
    second = app.secondsElapsed % 60
    drawLabel(f'You found {5-app.treasureLeft} treasures in {minute}min{second}sec!', app.width//2, app.height//2, size = 24, bold = True)
    bestMinute = app.bestRecordTime // 60
    bestSecond = app.bestRecordTime%60
    drawLabel(f'Your best record is {app.bestRecordTreasure} treasures found in {bestMinute}min{bestSecond}sec!', app.width//2, app.height//2+40, size = 24, bold = True)
    drawLabel('press space to start a new game', app.width//2, app.height//2+60, size = 16)
    drawLabel('press enter to go back to home screen', app.width//2, app.height//2+80, size = 16)

def end_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game') 
        restApp(app) 
    if key == 'enter':
        print("Switching to start screen")
        setActiveScreen('start')
#game screen ################

def game_redrawAll(app):
        drawBoard(app)
        drawBoardBorder(app)
        drawLabel('Collect Treasure!!', app.width//2, 25, size = 18)
        drawLabel('Press space bar to reset board', app.width//2, 45, size = 12)
        drawLabel('Press wasd to move around', app.width//2, 55, size = 12)
        drawLabel('Press b to toggle dark mode', app.width//2, 65, size = 12)
        minutes = app.seconds//60
        seconds = app.seconds%60
        drawLabel(f'you have {minutes}min {seconds}sec left', app.width//2, 500)
        if not app.darkMode:
            drawRoomOnTree(app, app.roomTreeRoot)
            drawWall(app)
            drawBorder(app)
            drawPacManPlayer(app)
            drawCastingLines(app)
            drawTreasure(app)
            drawLabel(f'{app.treasureLeft} treasures left to find', app.width//2, 463, size = 18, fill = 'white', bold = True)
        if app.darkMode:
            drawWall(app)
            drawBorder(app)
            drawRoomOnTree(app, app.roomTreeRoot)
            drawRect(100, 75, 400, 400, fill = 'black')
            drawCastingPoly(app)
            drawTreasureInDark(app)
            drawPacManPlayer(app)
            drawWallsInDark(app)
            drawLabel(f'{app.treasureLeft} treasures left to find', app.width//2, 463, size = 18, fill = 'white', bold = True)


# draw board ###################

def drawBorder(app):
    for row in range (app.rows):
        for col in range(app.cols):
            if row == 0 or row == app.rows-1 or col == 0 or col == app.cols-1:
                app.wallPositions.add((row, col))
                drawDungeonCell(app, row, col, fillColor='brown')
                app.board[row][col] = 'wall'
                


def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

# Draw Dungeon ###########################

def drawRoomOnTree(app, node):
    if node.isLeaf():
        drawRoom(app, node.roomLeft, node.roomTop, node.roomWidth, node.roomHeight)
        return
    else:
        drawRoomOnTree(app, node.childA)
        drawRoomOnTree(app, node.childB)
        return

def drawRoom(app, roomLeft, roomTop, roomWidth, roomHeight):
    drows = (-1, 0, 1)
    dcols = (-1, 0, 1)
    fillColor = None
    for row in range(roomTop, roomTop+roomHeight):
        for col in range(roomLeft, roomLeft+roomWidth):
            if row == roomTop or col == roomLeft:
                continue
            else:
                drawDungeonCell(app, row, col, fillColor)
                app.floorPositions.add((row, col))
    
    for row in range(roomTop, roomTop + roomHeight):
        for col in range(roomLeft, roomLeft + roomWidth):
            if (row == roomTop or row == roomTop + roomHeight - 1 or
                col == roomLeft or col == roomLeft + roomWidth - 1):
                if (row, col) not in app.floorPositions:
                    app.wallPositions.add((row, col))


def splitDungeon(app, roomLeft, roomTop, roomWidth, roomHeight, depth, maxDepth = 16):
    minSize = 6
    newNode = roomTree(roomLeft, roomTop, roomWidth, roomHeight, depth)
    if depth == maxDepth or roomWidth <=minSize or roomHeight <=minSize:
        return newNode
    else:
        splitHorizontally = random.choice([True, False])#used this to learn about random methods because we didn't learn them in class
                                                        #https://www.w3schools.com/python/module_random.asp 
        if splitHorizontally:
            splitNum = random.randint(2, roomHeight//2)
            if roomHeight - splitNum <= minSize :
                return newNode
            newNode.childA = splitDungeon(app, roomLeft, roomTop, roomWidth, splitNum, depth+1, maxDepth)
            newNode.childB = splitDungeon(app, roomLeft, roomTop+splitNum, roomWidth, roomHeight - splitNum, depth+1, maxDepth)
        
        else:#split vertically
            splitNum = random.randint(2, roomWidth//2)
            if roomWidth-splitNum <= minSize :
                return newNode
            newNode.childA = splitDungeon(app, roomLeft, roomTop, splitNum, roomHeight, depth+1, maxDepth)#height is the split num
            newNode.childB = splitDungeon(app, roomLeft+splitNum, roomTop, roomWidth-splitNum, roomHeight, depth+1, maxDepth)#height is total height - height of other room
        return newNode
    
def drawDungeonCell(app, row, col, fillColor='pink'):#to differ from regular draw cell call 
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=fillColor, border='black',
             borderWidth=app.cellBorderWidth)

#Draw walls
def drawWall(app):
    for wall in app.wallPositions:
        if wall not in app.floorPositions:
            (row, col) = wall
            drawDungeonCell(app, row, col, 'brown')
            app.board[row][col] = 'wall'


#connect rooms

def connectRooms(app, node):#get center of both rooms and carve a tunnel between them, setting every tile between the centers to a floor tile
    if node is None or node.isLeaf():
        return
    else:
        centerA = node.childA.roomCenter 
        centerB = node.childB.roomCenter
        makeTunnel(app, centerA, centerB)
        connectRooms(app,node.childA)
        connectRooms(app,node.childB)

def makeTunnel(app, centerA, centerB):
    (rowA, colA) = centerA
    (rowB, colB) = centerB
    for row in range(min(rowA, rowB), max(rowA, rowB)+1):
        if (row, colA) in app.wallPositions:
            app.wallPositions.remove((row, colA))
        app.floorPositions.add((row, colA))
    for col in range(min(colA, colB), max(colA, colB)+1):
        if (rowA, col) in app.wallPositions:
            app.wallPositions.remove((rowA, col))
        app.floorPositions.add((rowA, col))


# making the player  ###################

def drawPlayer(app):
    drawCircle(app.cx, app.cy, 5, rotateAngle = app.angle, fill = None, border = 'black')

#wall collision detection(Player)

#Chat GPT prompt for getCellInfo function:
#how can I convert a player position info(app.cx, app.cy, which is in pixels) to row and col on a 2D board
#Key Ideas for Free Pixel Movement:
#Player position is stored as (cx, cy) in pixels
#You still use a direction vector and rotateDirVector() for direction
#For collision detection, you must convert pixel position to grid cell
#You check if the cell is a wall before allowing movement
def getCellInfo(app, x, y):
    cellWidth, cellHeight = getCellSize(app)
    col = int((x-app.boardLeft)/cellWidth)
    row = int((y-app.boardTop)/cellHeight)
    return row, col

def isNotCollision(app, x, y, angle):
    r = 10#pacMan's radius
    if angle == None:
        angle = app.angle
    (edgeX, edgeY) = getRadiusEndpoint(app, x, y, r, angle)
    row, col = getCellInfo(app, edgeX, edgeY)
    if 0<=row<app.rows and 0 <= col < app.cols:
        if app.board[row][col] == 'floor' or  app.board[row][col] == None or app.board[row][col] == 'Treasure':
            return True
        else:
            app.showWall.add((row,col))#when it is collision, store it in the set to help the darkmode wall displays
            return False
    return False

def isNotBeamCollision(app, x, y):
    row, col = getCellInfo(app, x, y)
    if 0<=row<app.rows and 0 <= col < app.cols:
        if app.board[row][col] == 'floor' or  app.board[row][col] == None or app.board[row][col] == 'Treasure':
            return True
        else:
            app.showWall.add((row,col))
            return False
    return False

def game_onStep(app):
    endGame(app)
    if app.gameOver:
        setActiveScreen('end')
    # Timer
    app.stepsTaken += 1
    if app.stepsTaken>= app.stepsPerSecond and app.stepsTaken%50 == 0:
        app.seconds -= 1
        app.secondsElapsed += 1
    #pacManPlayer
    PacManOnStep(app)
    #moving the player
    if app.isRotating:
        if app.key == 'a':
            app.angle += app.rotationStep 
        elif app.key == 'd':
            app.angle -= app.rotationStep
    if app.isMoving:
        rad = math.radians(app.angle)
        dx = app.d * math.cos(rad)
        dy = -app.d * math.sin(rad)
        newCx, newCy = app.cx, app.cy
        if app.key == 'w':
            newCx = app.cx + dx
            newCy = app.cy + dy
        elif app.key == 's':
            newCx = app.cx - dx
            newCy = app.cy - dy
        # copilot prompt for the calculation of dx and dy above: how do i modify onStep to make the direction 
        # of movement when s and w are pressed align with the direction of the beam
        # the two conditionals above were originally written like below. 
        # i knew there was something wrong with the vector addition, but wasn't familiar enough with trig to find
        # the mathematical mistake going on here, hence asked copilot how this would be fixed
        '''if app.key == 'w':
            dx = app.dirVector[0]*app.d
            dy = -app.dirVector[1]*app.d
        elif app.key == 's':
            dx = -app.dirVector[0]*app.d
            dy = app.dirVector[1]*app.d'''
        if (app.key == 'w' or app.key == 's') and isNotCollision(app, newCx, newCy, app.angle):
            app.cx = newCx
            app.cy = newCy
            if isTreasureCollision(app, app.cx, app.cy):
                eatTreasure(app, app.cx, app.cy)

def game_onKeyPress(app, key):
    if key == 'space':
        restApp(app)
    if key == 'b':
        app.darkMode = True if app.darkMode == False else False
    app.key = key
    if key == 'a' or key == 'd':
        app.isRotating = True
    elif key == 'w' or key == 's':
        app.isMoving = True



def game_onKeyRelease(app, key):
    if key == 'a' or key == 'd':
        app.isRotating = False
    elif key == 'w' or key == 's':
        app.isMoving = False

#wall collision(raycasting)
#copilot prompt:
#how can i make the incrementing steps smaller
# (i used a for loop which only allows r to increment by an integer,
#  which makes the rays poke into the walls a bit too much)
#copliot response:
#To make the raycasting steps smaller (for more precise collision detection), 
#increment r by a small value (like 0.5 or 1) instead of adding i in each loop.
#Replace your inner loop with a while loop and increment r by a float
def drawCastingLines(app):    
    app.showWall.clear()
    app.showTreasure.clear()
    baseAngle = app.angle
    fov = 60
    startAngle = baseAngle - fov/2
    maxRayLength = 120
    numOfRays = 10
    for i in range (numOfRays):
        angle = startAngle + i * (fov / numOfRays)
        r = app.rayCastRadius#rest radius to start trying to increment again
        step = 0.5
        targetX, targetY = getRadiusEndpoint(app, app.cx, app.cy, r, angle)#rest targetX targetY
        while r < maxRayLength:
            r+= step # increment
            testX, testY = getRadiusEndpoint(app, app.cx, app.cy, r, angle)# get the targetX, targetY after increment
            if not isNotBeamCollision(app, testX, testY):#check if it collides with a wall
                break
            targetX, targetY = testX, testY
        drawLine(app.cx, app.cy, targetX, targetY, lineWidth = 0.8, fill = 'yellow')

def drawCastingPoly(app):
    app.showWall.clear()
    app.showTreasure.clear()
    polygonPoints = [(app.cx, app.cy)]
    baseAngle = app.angle
    fov = 60
    startAngle = baseAngle - fov/2
    maxRayLength = 120
    numOfRays = 20
    for i in range (numOfRays):
        angle = startAngle + i * (fov / numOfRays)# previously I was only working with theta and not angle
        #which causes the problem of each trial ray not spreading out far enough and twisting to make
        #the polygon look like various lines rather than a torch light beam
        #hence I gave ChatGPT the code in this function and asked: "how to make the 
        # polygon not twist over itself and make the Field of View larger"
        # it explained to me:
        '''
        theta is the starting angle of the field of view. In your case, it's computed as:
        theta = 180 - baseAngle
        This helps orient the view based on the player's current direction (angle).
        numRays is how many individual rays you're casting (e.g. 50 rays total).
        60 / numRays is the angular step between rays. For example:
        If numRays = 60, then each ray is 1° apart.
        If numRays = 20, each ray is 3° apart.
        i goes from 0 to numRays - 1. This gradually increases the angle.
        So the expression:
        angle = theta + i * (60 / numRays)
        "Start at theta, and cast rays one-by-one, increasing by a fixed angle each time, so they spread evenly over a 60° arc."
        '''
        r = app.rayCastRadius#rest radius to start trying to increment again
        step = 0.5
        targetX, targetY = getRadiusEndpoint(app, app.cx, app.cy, r, angle)#rest targetX targetY
        while r < maxRayLength:
            r+= step # increment
            testX, testY = getRadiusEndpoint(app, app.cx, app.cy, r, angle)# get the targetX, targetY after increment
            if isTreasureCollision(app, testX, testY):
                app.showTreasure.add((testX, testY))
            if not isNotBeamCollision(app, testX, testY):#check if it collides with a wall
                targetX, targetY = testX, testY
                break#if not collision update targetX, targetY
            targetX, targetY = testX, testY
        polygonPoints.append((targetX, targetY))
    drawPolygon(*[coord for pair in polygonPoints for coord in pair], fill = 'yellow' ) 
        # copilot prompt for this line above
        # on line 320, how can i modify the code so that the draw polygon 
        # incorporates the pairs of coordinates in app.polygonPoints?

def drawWallsInDark(app):
    for wall in app.showWall:
        if wall not in app.floorPositions:
            (row, col) = wall
            drawDungeonCell(app, row, col, 'brown')
            app.board[row][col] = 'wall'

#draw treasure

def isTreasure(app, x, y):
    row, col = getCellInfo(app, x, y)
    if 0<=row<app.rows and 0 <= col < app.cols:
        if app.board[row][col] == 'treasure':
            return True
    return False

def drawTreasureCell(app, row, col, fillColor):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=fillColor, border='Black',
             borderWidth=app.cellBorderWidth)

def drawTreasure(app):
    for treasure in app.treasurePosition:
        (row, col) = treasure
        drawTreasureCell(app, row, col, 'lightBlue')
        app.board[row][col] = 'Treasure'


def placeTreasure(app):
    app.treasurePosition.clear()
    treasures = random.sample(list(app.floorPositions), 5)
    for treasure in treasures:
        app.treasurePosition.add(treasure)


def isTreasureCollision(app, x, y):
    row, col = getCellInfo(app, x, y)
    if 0<=row<app.rows and 0<=col<app.cols and app.board[row][col] == 'Treasure':
        return True
    else:
        return False

def eatTreasure(app, x, y):
    row, col = getCellInfo(app, x, y)
    if (row, col) in app.treasurePosition:
        app.treasureLeft -= 1
        app.board[row][col] = 'floor'
        app.treasurePosition.remove((row, col))


def drawTreasureInDark(app):
    for treasure in app.showTreasure:
        (x, y) = treasure
        (row, col) = getCellInfo(app, x, y)
        drawTreasureCell(app, row, col, 'LightBlue')
        app.board[row][col] = 'Treasure'

def endGame(app):
    if app.treasureLeft == 0 or app.seconds <= 0:
        checkBestRecord(app)
        app.gameOver = True
        setActiveScreen('end')
        
## keep track of best record########
# largest num of treasures found in shortest amount of time
def checkBestRecord(app):
    if ((app.bestRecordTime == None and app.bestRecordTreasure == None) or 
        (app.secondsElapsed <= app.bestRecordTime and app.bestRecordTreasure >= (5-app.treasureLeft))):
        app.bestRecordTime = app.secondsElapsed
        app.bestRecordTreasure = 5-app.treasureLeft


def main():
    runAppWithScreens(initialScreen='start')
main()
