import pygame as py
from constant import *
from flappy import Flappy       



py.init()

# Create flappy game
flappy = Flappy()
# Set up the drawing window
screen = py.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = py.font.Font(None, 30)
def textDisplay(flappy: Flappy):
    img = font.render("Current Score: "+str(flappy.getCurrentBestScore())+"     Best Score: "+str(flappy.getBestScore())+"       Gen: " + str(flappy.generation)+"       Birds: "+str(len(flappy.birds)), True, (0,0,0))
    screen.blit(img, (5, 5))

def draw(flappy: Flappy):
    py.draw.rect(screen,(168, 245, 255),(0,0, SCREEN_WIDTH,SKY))
    py.draw.rect(screen,(133, 90, 53),(0,SCREEN_HEIGHT-GROUND, SCREEN_WIDTH,GROUND))
    birds = flappy.getBirds()
    pipes = flappy.getPipes()
    for each in birds:
        x,y = each.getCoordinates()
        py.draw.circle(screen, (142, 145, 105), (int(x), int(y)), BIRD_RADIUS)
    for each in pipes:
        x,y = each.getCoordinates()
        width,height = each.getSize()
        py.draw.rect(screen,(30, 150, 68),(int(x),int(y), int(width),int(height)))
    textDisplay(flappy)
# Run until the user asks to quit
running = True
while running:
    
    # Did the user click the window close button?
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                flappy.move(True)

    if flappy.getBestScore() >= 100:
        continue
    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    draw(flappy)
    flappy.move()

    # Flip the display
    py.display.flip()

# Done! Time to quit.
py.quit()