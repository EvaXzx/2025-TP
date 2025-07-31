from cmu_graphics import *
#code from cs academy
def PacManOnAppStart(app):
    app.mouthAngle = 90
    app.rotateAngle = 0
    app.cx = 200
    app.cy = 200
    app.closing = True

def drawPacManPlayer(app):
    startAngle = app.mouthAngle/2
    sweepAngle = 360 - app.mouthAngle
    drawArc(app.cx, app.cy, 20, 20, startAngle, sweepAngle,
            rotateAngle=-app.angle,
            fill='cyan', border='black')


def PacManOnStep(app):
    if app.closing:
        app.mouthAngle -= 10
        if app.mouthAngle == 0:
            app.closing = False
    else:
        app.mouthAngle += 10
        if app.mouthAngle == 90:
            app.closing = True
