#Draw Board
from cmu_graphics import *
import random


class roomTree:
    def __init__(self, roomLeft, roomTop, roomWidth, roomHeight, depth=0):
        self.roomLeft = roomLeft
        self.roomTop = roomTop
        self.roomWidth = roomWidth
        self.roomHeight = roomHeight
        self.depth = depth
        self.childA = None
        self.childB = None
    
    def isLeaf(self):
        return self.childA == None and self.childB == None


def onAppStart(app):
    app.rows = 16
    app.cols = 16
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 2
    app.width = 500
    app.height = 500
    app.curRoomLength = 12
    app.roomTreeRoot = splitDungeon(app, 0, 0, app.cols, app.rows, 0, 8)

def redrawAll(app):
    drawRect(50, 74, 400, 400, fill =None)
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel('Escaping studio before 3AM', app.width//2, 50, size = 20)
    drawRoomOnTree(app, app.roomTreeRoot)

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
    fillColor = rgb(random.randint(100, 255),random.randint(100, 255), random.randint(100, 255))
    for row in range(roomTop, roomTop+roomHeight):
        for col in range(roomLeft, roomLeft+roomWidth):
            if (0<=row<app.rows) and (0<= col < app.cols):
                drawDungeonCell(app, row, col, fillColor)

def splitDungeon(app, roomLeft, roomTop, roomWidth, roomHeight, depth, maxDepth = 8):
    minSize = 3
    newNode = roomTree(roomLeft, roomTop, roomWidth, roomHeight, depth)
    if depth >= maxDepth or roomWidth <=minSize or roomHeight <=minSize:
        return newNode
    else:
        splitHorizontally = random.choice([True, False])
        if splitHorizontally:
            splitNum = random.randint(2, roomHeight-2)
            if roomHeight - splitNum <= minSize :
                return newNode
            newNode.childA = splitDungeon(app, roomLeft, roomTop, roomWidth, splitNum, depth+1, maxDepth)
            newNode.childB = splitDungeon(app, roomLeft, roomTop+splitNum, roomWidth, roomHeight - splitNum, depth+1, maxDepth)
        
        else:#split vertically
            splitNum = random.randint(2, roomWidth-2)
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






def main():
    runApp()

main()