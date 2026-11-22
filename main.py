from functools import partial
from sys import exit

import numpy as np
import pygame
from vpython import *

from propagator import OscillatorMatrix, coupledOscillator
from simulation import Simulation

NUM_OSCILLATORS=3
running=False
def simulateOscillator():
    '''A pygame simulation for the oscillators. '''
    State=True
    Start=False
    pygame.init()
    GAME_WIDTH=1000
    GAME_HEIGHT=500
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
        def realToPixel(self,identity,pos):
            return SHIFT+ identity*(int(GAME_WIDTH/NUM_OSCILLATORS))+pos*SCALING
        def draw(self):
            pygame.draw.rect(window,"dark green",self.rect)
    blocks=[]
    forces = [
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
    ]
    initial=np.array([-.5,0,.5])
    for i,s in enumerate(initial):
        blocks.append(Block(i,s))
    mass=np.array([1,1,1])
    k=np.array([5,5,5,5])
    A=OscillatorMatrix(mass,k)
    initialTime=0
    initialState=np.concatenate([np.array([block.pos for block in blocks]),np.zeros(NUM_OSCILLATORS)])
    propagator_One=partial(coupledOscillator,force=forces,A=A)
    Oscillator=Simulation(initialTime,initialState,propagator_One)
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

def vPythonOscillator(sim):

    scene = canvas(
        title="Coupled Oscillators",width=1400,height=800,background=color.black)
    scene.center = vector(0, 0, 0)
    scene.range = 8
    scene.autoscale = False
    scene.forward = vector(0, 0, -5)
    d = 2.0

    left_wall_x = -(NUM_OSCILLATORS + 1) * d / 2
    right_wall_x = (NUM_OSCILLATORS + 1) * d / 2

    wall = box(pos=vector(left_wall_x, 0, 0),size=vector(0.2, 3, 2),color=color.gray(0.5)
    )

    wall2 = box(pos=vector(right_wall_x, 0, 0),size=vector(0.2, 3, 2),color=color.gray(0.5)
    )
    def handleEvent(evt):
        global running 
        if evt.key == ' ':
            running = not running
    
    scene.bind('keydown',handleEvent)
    balls=[]
    for i in range(NUM_OSCILLATORS):
        equilibrium_x = (i - (NUM_OSCILLATORS - 1)/2) * d
        balls.append(sphere(pos=vector(equilibrium_x + sim.getState()[i], 0, 0), radius=0.3,    color=color.red))
    while True:
        rate(60)
        if running:
            for _ in range(10):
                sim.step()
            state=sim.getState()
            for i, ball in enumerate(balls):
                equilibrium_x = (i - (NUM_OSCILLATORS - 1)/2) * d
                ball.pos.x = equilibrium_x + state[i]

def main():
    mass=np.array([1,1,1])
    k=np.array([3,3,3,3])
    forces = [
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
    ]
    A=OscillatorMatrix(mass,k)
    propagator=partial(coupledOscillator,force=forces,A=A)
    initialTime=0
    initialState=np.array([.5,-.5*np.sqrt(2),.5])
    initialState=np.concatenate([initialState,np.zeros(NUM_OSCILLATORS)])
    oscillatorSimulation=Simulation(initialTime,initialState,propagator)
    vPythonOscillator(oscillatorSimulation)
if __name__ == "__main__":
    main()