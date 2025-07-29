#Draw Board
from cmu_graphics import *
import random

def onAppStart(app):
    app.rows = 12
    app.cols = 12
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 2
    app.width = 500
    app.height = 500
    app.curRoomLength = 12

def redrawAll(app):
    drawRect(50, 74, 400, 400, fill ='lightBlue')
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel('Escaping studio before 3AM', app.width//2, 50, size = 20)
    splitDungeonHorizontal(app)
    

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

def drawDungeonCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill='pink', border='black',
             borderWidth=app.cellBorderWidth)

def splitDungeonHorizontal(app):
    #draw starting cell
    curRoomLength = app.rows
    row = random.randint(3, curRoomLength-3)
    col = 0
    drawDungeonCell(app, row, col)
    for i in range (app.curRoomLength):
        drawDungeonCell(app, row, col+i)
    if app.rows - row < 2:
        splitDungeonHorizontal(app)

def splitDungeonVertical(app):
    curRoomHeight = app.cols
    col = random.randint(3, curRoomHeight-3)
    row = 0
    drawDungeonCell(app, row, col)
    for i in range (app.curRoomLength):
        drawDungeonCell(app, row+1, col)
    if app.cols - col < 2:
        splitDungeonVertical(app)

def splitDungeon(app, maxDepth = 3, depth=0):
    if depth == maxDepth:
        return
    else:
        curSplit = random.choice(['horizontal', 'vertical'])
        if curSplit == 'horizontal':
            splitDungeonHorizontal(app)
        elif curSplit == 'vertical':
            splitDungeonVertical(app)
        return splitDungeon(app, maxDepth = 3, depth)




def main():
    runApp()

main()