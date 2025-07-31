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