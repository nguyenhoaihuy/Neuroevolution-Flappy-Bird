from constant import *
class Pipe:
    def __init__(self,height:int,x=0,y=0):
        self.x = x
        self.y = y
        self.height = height
        self.width = PIPE_WIDTH
        self.speed = SCREEN_SPEED
    
    def getCoordinates(self):
        return self.x, self.y

    def getSize(self):
        return self.width,self.height
    
    def isOutOfScreen(self) -> bool:
        if self.x + self.width < 0:
            return True
        else: return False
        
    def move(self):
        self.x -= self.speed