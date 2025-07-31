from cmu_graphics import *
import math

def onAppStartHelper(app):
    app.isMoving = False
    app.cx = app.width//2
    app.cy = app.height//2
    app.dirVector = [0, 1]#(x, y)
    app.dirVC = 0.1 #direction vector change
    app.d = 5
    app.angle = 0
    app.rotationStep = 10
    app.isRotating = False
    app.isMoving = False
    app.key = None
    app.rayCastRadius = 1
    

 # rotating the player 
 # https://matthew-brett.github.io/teaching/rotation_2d.html
 # read this to understand how to use direction vector to rotate the player 
def rotateDirVector(vector, angleDegrees):
    angleRadians = math.radians(angleDegrees)
    x, y = vector
    newX = x * math.cos(angleRadians) - y * math.sin(angleRadians)
    newY = x * math.sin(angleRadians) + y * math.cos(angleRadians) 
    return [newX, newY]     

#raycasting flashlight
#draw line 
def getRadiusEndpoint(app, cx, cy, r, theta):
    return (app.cx + r*math.cos(math.radians(theta)),
            app.cy - r*math.sin(math.radians(theta)))






    


 
        




