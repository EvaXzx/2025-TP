#tree that stores room information
#each room has two children rooms because I am dividing each room binarily
#https://www.geeksforgeeks.org/dsa/binary-space-partitioning/ 
#https://www.geeksforgeeks.org/dsa/binary-space-partitioning/ 
#ChatGPT Prompt: how can i build a bsp tree that stores information about rooms on a board
#https://chatgpt.com/share/68892d01-4508-8002-bf0c-ca9f4daca284 
#Read these websites to help me understand how to use BSP Tree class


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