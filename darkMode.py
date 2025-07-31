from cmu_graphics import *
#only draw player, walls touched by the ray cast, make ray cast draw a polygon instead
def drawPlayerDarkMode(app):
    drawCircle(app.cx, app.cy, 5, rotateAngle = app.angle, fill = None, border = 'white')