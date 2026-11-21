from sys import exit
import numpy as np
import pygame
from propagator import OscillatorMatrix
pygame.init()
GAME_WIDTH=750
GAME_HEIGHT=300
NUM_OSCILLATORS=3
SCALING=50 ##Going from meters to pixels on screen.
SHIFT=GAME_WIDTH/(2.5*NUM_OSCILLATORS) ##Initial shift for first block from left of the screen
window=pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Coupled Oscillators")
clock=pygame.time.Clock()

class Block:
    def __init__(self,identity :int,pos :float,vel:float,mass:float):
        self.id=identity
        self.pos=pos 
        self.vel=vel 
        self.pixelX=self.realToPixel(identity,pos)
        self.mass=mass
        self.rect=pygame.Rect(self.pixelX,int(GAME_HEIGHT/2),50,50)
    def updatePos(self,pos):
        self.pos=pos
        self.rect.x=self.realToPixel(self.id,pos)
    def updateVel(self,vel):
        self.vel=vel
    def realToPixel(self,identity,pos):
        return SHIFT+ identity*(int(GAME_WIDTH/NUM_OSCILLATORS))+pos*SCALING
    def draw(self):
        pygame.draw.rect(window,"red",self.rect)
blocks=[]
for i in range(NUM_OSCILLATORS):
    blocks.append(Block(i,0,0,1))      

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            blocks[0].updatePos(.1)
    window.fill("black")
    for block in blocks:
        block.draw()
    pygame.display.update()
    clock.tick(60)
            























def main():
    print("Hello from finalproject!")


if __name__ == "__main__":
    main()
