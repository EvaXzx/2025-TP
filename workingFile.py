#Draw Board
from cmu_graphics import *
import random

#tree that stores room information
#each room has two children rooms because I am dividing each room binarily
class roomTree:
    def __init__(self, roomLeft, roomTop, roomWidth, roomHeight, depth=0):
        self.roomLeft = roomLeft
        self.roomTop = roomTop
        self.roomWidth = roomWidth
        self.roomHeight = roomHeight
        self.depth = depth
        self.childA = None
        self.childB = None
        centerRow = roomTop+1 + roomHeight // 2
        centerCol = roomLeft+1 + roomWidth // 2

        self.roomCenter = (centerRow, centerCol)
    
    def isLeaf(self):
        return self.childA == None and self.childB == None


def onAppStart(app):
    app.rows = 20
    app.cols = 20
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 0.5
    app.width = 500
    app.height = 500
    app.curRoomLength = 12
    app.roomTreeRoot = splitDungeon(app, 0, 0, app.cols, app.rows, 0, 8)
    app.wallPositions = set()
    app.floorPositions = set()
    connectRooms(app, app.roomTreeRoot)

def redrawAll(app):
    drawRect(50, 74, 400, 400, fill =None)
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel('Escaping studio before 3AM', app.width//2, 50, size = 20)
    drawRoomOnTree(app, app.roomTreeRoot)
    drawWall(app)
    for row in range (app.rows):
        for col in range(app.cols):
            if row == 0 or row == app.rows-1 or col == 0 or col == app.cols-1:
                drawDungeonCell(app, row, col, fillColor='brown')

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

#Draw Dungeon

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
        splitHorizontally = random.choice([True, False])
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
            newNode.childA = splitDungeon(app, roomLeft, roomTop, splitNum, roomHeight, depth+1, maxDepth)
            newNode.childB = splitDungeon(app, roomLeft+splitNum, roomTop, roomWidth-splitNum, roomHeight, depth+1, maxDepth)
        return newNode
    
def drawDungeonCell(app, row, col, fillColor='pink'):
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

#connect rooms

def connectRooms(app, node):
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






def main():
    runApp()

main()