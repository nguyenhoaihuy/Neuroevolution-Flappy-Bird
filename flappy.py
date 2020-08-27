import random
import math
from constant import *
from pipe import Pipe
from bird import Bird
from typing import List
from neunet import NeuronNetwork

class Flappy:
    def __init__(self):
        self.num_of_birds = NUM_OF_BIRDS
        self.new_pipe_distance = DISTANCE_BTW_PIPES
        self.birds = []
        self.fail_birds = []
        self.pipes = []
        for i in range(self.num_of_birds):
            self.birds.append(Bird(300,400))
        self.addInitialPipes()
        self.generation = 1
        self.best_score = 0

    # start over
    def startOver(self):
        self.num_of_birds = NUM_OF_BIRDS
        self.new_pipe_distance = DISTANCE_BTW_PIPES
        self.birds = self.newGeneration()
        self.generation += 1
        self.fail_birds = []
        self.pipes = []
        self.addInitialPipes()
    
    # generate new generation
    def newGeneration(self)->List[Bird]:
        best_bird = Bird(300,400)
        best_fitness = 0
        if len(self.fail_birds) > 0:
            best_bird = self.fail_birds[0]
        for bird in self.fail_birds:
            bird_fitness = bird.getFitness()
            if bird_fitness >= best_fitness:
                best_fitness = bird_fitness
                best_bird = bird
        new_bird_generation = []
        for i in range(NUM_OF_BIRDS):
            # print(i)
            new_bird_generation.append(Bird(300,400,best_bird.brain))
        return new_bird_generation


    # Initialize 4 pipes
    def addInitialPipes(self):
        self.pipes.append(Pipe(PIPE_HEIGHT_DEFAULT,700,SKY))
        self.pipes.append(Pipe(SCREEN_HEIGHT-SKY-PIPE_HEIGHT_DEFAULT-GAP_BTW_PIPES-GROUND,700,PIPE_HEIGHT_DEFAULT+GAP_BTW_PIPES+SKY))
        random_height = random.randrange(PIPE_HEIGHT_DEFAULT-200, PIPE_HEIGHT_DEFAULT+200)
        self.pipes.append(Pipe(random_height,SCREEN_WIDTH,SKY))
        self.pipes.append(Pipe(SCREEN_HEIGHT-SKY-random_height-GAP_BTW_PIPES-GROUND,SCREEN_WIDTH,random_height+GAP_BTW_PIPES+SKY))

    # return list of birds
    def getBirds(self) -> List[Bird]:
        return self.birds
    
    # return list of pipes
    def getPipes(self) -> List[Pipe]:
        return self.pipes
    
    # add new Pipes
    def addNewPipes(self):
        random_height = random.randrange(90, 490)
        self.pipes.append(Pipe(random_height,SCREEN_WIDTH,SKY))
        self.pipes.append(Pipe(SCREEN_HEIGHT-random_height-GAP_BTW_PIPES-SKY-GROUND,SCREEN_WIDTH,random_height+GAP_BTW_PIPES+SKY))
    
    # remove pipes which are out of the screen
    def removePipes(self):
        self.pipes = [x for x in self.pipes if not x.isOutOfScreen()]

    # check if a bird and a pipe is collided or not
    def isCollided(self,bird:Bird,pipe:Pipe) -> bool:
        x,y = bird.getCoordinates()
        # get eight points' coordinates around the bird 
        n_x,n_y = x,y-BIRD_RADIUS
        s_x,s_y = x,y+BIRD_RADIUS
        w_x,w_y = x-BIRD_RADIUS,y
        e_x,e_y = x+BIRD_RADIUS,y 
        nw_x,nw_y = int(x-BIRD_RADIUS*math.sqrt(2)/2),int(y-BIRD_RADIUS*math.sqrt(2)/2)
        ne_x,ne_y = int(x+BIRD_RADIUS*math.sqrt(2)/2),int(y-BIRD_RADIUS*math.sqrt(2)/2)
        sw_x,sw_y = int(x-BIRD_RADIUS*math.sqrt(2)/2),int(y+BIRD_RADIUS*math.sqrt(2)/2)
        se_x,se_y = int(x+BIRD_RADIUS*math.sqrt(2)/2),int(y+BIRD_RADIUS*math.sqrt(2)/2)

        # get the pipe's coordinates and size
        x_pipe,y_pipe = pipe.getCoordinates()
        width_pipe,height_pipe = pipe.getSize()

        # check if one of the eight point is inside the pipe
        if n_x > x_pipe and n_x < x_pipe + width_pipe and n_y > y_pipe and n_y < y_pipe + height_pipe:
            return True
        if s_x > x_pipe and s_x < x_pipe + width_pipe and s_y > y_pipe and s_y < y_pipe + height_pipe:
            return True
        if w_x > x_pipe and w_x < x_pipe + width_pipe and w_y > y_pipe and w_y < y_pipe + height_pipe:
            return True
        if e_x > x_pipe and e_x < x_pipe + width_pipe and e_y > y_pipe and e_y < y_pipe + height_pipe:
            return True
        if nw_x > x_pipe and nw_x < x_pipe + width_pipe and nw_y > y_pipe and nw_y < y_pipe + height_pipe:
            return True
        if ne_x > x_pipe and ne_x < x_pipe + width_pipe and ne_y > y_pipe and ne_y < y_pipe + height_pipe:
            return True
        if sw_x > x_pipe and sw_x < x_pipe + width_pipe and sw_y > y_pipe and sw_y < y_pipe + height_pipe:
            return True
        if se_x > x_pipe and se_x < x_pipe + width_pipe and se_y > y_pipe and se_y < y_pipe + height_pipe:
            return True
        return False
                
    # get the best score
    def getCurrentBestScore(self):
        score = 0
        for bird in self.birds:
            bird_score = bird.getScore()
            if bird_score > score:
                score = bird_score
            if bird_score > self.best_score:
                self.best_score = bird_score
        return score

    def getBestScore(self):
        return self.best_score

    # the main function to change the status of the game
    def move(self,moveup=False):
        # start over if there is no bird alive
        if len(self.birds) == 0:
            self.startOver()
        # print(len(self.fail_birds),len(self.birds))
        # get birds move
        for bird in self.birds:
            x,y = bird.getCoordinates()
            pipe_x,pipe_y = self.pipes[0].getCoordinates()
            if x > pipe_x+PIPE_WIDTH:
                bird.startScore()
            bird_x, bird_y = bird.getCoordinates()
            y1,y2 = self.getClosestCoordinate(bird)
            guess_input = [bird_x,bird_y,y1,y2]
            if bird.brain.guess(guess_input):
                bird.moveUp()
            bird.move()
        
        # get pipes move
        for pipe in self.pipes:
            pipe.move()
        
        # remove the birds which hit pipes
        for pipe in self.pipes:
            self.fail_birds += [x for x in self.birds if self.isCollided(x,pipe)]
            self.birds = [x for x in self.birds if not self.isCollided(x,pipe)]

        # remove the pipes which are out of the screen
        self.removePipes()
        self.new_pipe_distance -= SCREEN_SPEED
        if self.new_pipe_distance <= 0:
            self.addNewPipes()
            self.new_pipe_distance = DISTANCE_BTW_PIPES
        
        # get best score
        for bird in self.birds:
            bird_score = bird.getScore()
            if bird_score > self.best_score:
                self.best_score = bird_score

    def getClosestCoordinate(self,bird:Bird):
        y1 = 0
        y2 = 0
        smallest_dis = 1000
        closest_pipe = self.pipes[0]
        for pipe in self.pipes:
            x_pipe,y_pipe = pipe.getCoordinates()
            x_bird,y_bird = bird.getCoordinates()
            dis = x_pipe + PIPE_WIDTH - x_bird
            if dis >= 0 and dis < smallest_dis:
                smallest_dis = dis 
                closest_pipe = pipe 
        x_pipe, y_pipe = closest_pipe.getCoordinates()
        width_pipe, height_pipe = closest_pipe.getSize()
        if y_pipe == SKY:
            y1 = SKY + height_pipe
            y2 = y1 + GAP_BTW_PIPES
        else:
            y2 = y_pipe
            y1 = y2 - GAP_BTW_PIPES
        return y1,y2


