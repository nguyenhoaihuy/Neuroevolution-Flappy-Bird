from neunet import NeuronNetwork
from constant import *
import copy 
class Bird:
    def __init__(self,x=0,y=0,brain=None):
        self.x = x
        self.y = y
        self.r = BIRD_RADIUS
        self.acceloration = -0.15
        self.velocity = 0
        self.score = 0
        self.start_score = False
        self.score_delay = 0
        self.brain = NeuronNetwork(4,1,[4])
        if brain:
            self.brain = copy.deepcopy(brain)
            self.brain.mutate(MUTATION_RATE)
        self.fitness = 0
    
    def startScore(self):
        if not self.start_score:
            self.score_delay = DISTANCE_BTW_PIPES
            self.score += 1
        self.start_score = True

    def getScore(self):
        return self.score

    def getFitness(self):
        return self.fitness
    
    def reset(self):
        self.fitness = 0
        self.start_score = False
        self.score = 0
        self.score_delay = 0
        self.velocity = 0
        return

    def getCoordinates(self):
        return self.x, self.y
        
    def moveUp(self):
        self.velocity = -4

    def move(self):
        self.fitness += 1
        self.velocity -= self.acceloration
        self.y += self.velocity
        if self.start_score:
            if self.score_delay <= 0:
                self.score += 1
                self.score_delay = DISTANCE_BTW_PIPES
            self.score_delay -= SCREEN_SPEED
        if self.isOnTheSky():
            self.y = SKY+self.r
            self.velocity = 0
        if self.isOnTheGround():
            self.y = SCREEN_HEIGHT - GROUND - self.r

    def isOnTheSky(self):
        if self.y - self.r <= SKY:
            return True
        else:return False

    def isOnTheGround(self):
        if self.y + self.r >= SCREEN_HEIGHT - GROUND:
            return True
        else:return False