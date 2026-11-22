from functools import partial
from sys import exit

import numpy as np
import pygame

from propagator import OscillatorMatrix, coupledOscillator
from simulation import Simulation

TIME_ELAPSED=0
State=True
Start=False
pygame.init()
GAME_WIDTH=1000
GAME_HEIGHT=300
NUM_OSCILLATORS=3
SCALING=100 ##Going from meters to pixels on screen.
SHIFT=GAME_WIDTH/(2.5*NUM_OSCILLATORS) ##Initial shift for first block from left of the screen
window=pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Coupled Oscillators")
clock=pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
text = font.render(
    "Press SPACE to start simulation",
    True,
    "white"
)
text_rect = text.get_rect(
    center=(GAME_WIDTH // 2, 40)
)
class Block:
    def __init__(self,identity :int,pos :float):
        self.id=identity
        self.pos=pos 
        self.pixelX=self.realToPixel(identity,pos)
        self.rect=pygame.Rect(self.pixelX,int(GAME_HEIGHT/2),50,50)
    def updatePos(self,pos):
        self.pos=pos
        self.rect.x=round(self.realToPixel(self.id, pos))
    def updateVel(self,vel):
        self.vel=vel
    def realToPixel(self,identity,pos):
        return SHIFT+ identity*(int(GAME_WIDTH/NUM_OSCILLATORS))+pos*SCALING
    def draw(self):
        pygame.draw.rect(window,"red",self.rect)
blocks=[]
omega3 = np.sqrt(2 + np.sqrt(2))
forces = [
    lambda t:0.0,
    lambda t:0.0,
    lambda t:0.0,
    lambda t:0.0,
    lambda t:np.sin(omega3*t) if t<3  else 0,
    lambda t:0.0
]

blocks.append(Block(0,.5))
blocks.append(Block(1,.5*np.sqrt(2)))
blocks.append(Block(2,.5))

mass=np.array([5,5,5])
k=np.array([5,5,5,5])
A=OscillatorMatrix(mass,k)
initialTime=0
initialState=np.concatenate([np.array([block.pos for block in blocks]),np.zeros(NUM_OSCILLATORS)])
propagator=partial(coupledOscillator,force=forces,A=A)
Oscillator=Simulation(initialTime,initialState,propagator)
while State:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Start = True
                accumulator = 0.0
            if event.key == pygame.K_x:
                pygame.quit()
                exit()
    if Start:
        accumulator += dt
        while accumulator >= Oscillator.h:
            Oscillator.step()
            accumulator -= Oscillator.h
        posUpdate = Oscillator.getState()
        for i, block in enumerate(blocks):
            block.updatePos(posUpdate[i])
    window.fill("black")
    if not Start:
        window.blit(text, text_rect)
    for block in blocks:
        block.draw()
    pygame.display.flip()
            























def main():
    print("Hello from finalproject!")


if __name__ == "__main__":
    main()
