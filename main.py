from functools import partial

import numpy as np
from vpython import *

from propagator import OscillatorMatrix, coupledOscillator, lorentzAttractor
from simulation import Simulation

NUM_OSCILLATORS=5
running=False

def vPythonOscillator(sim):
    RADIUS=.15
    scene = canvas(
        title="Coupled Oscillators",width=1400,height=800,background=color.black)
    scene.center = vector(0, 0, 0)
    scene.range = 8
    scene.autoscale = False
    scene.forward = vector(0, 0, -2)
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
    springs=[]
    dark_green = vector(0, 0.4, 0)
    for i in range(NUM_OSCILLATORS+1):
        equilibrium_x = (i - (NUM_OSCILLATORS - 1)/2) * d

        if i==0:
            balls.append(sphere(pos=vector(equilibrium_x + sim.getState()[i], 0, 0), radius=.3,color=dark_green))
            displacement=vector((balls[0].pos.x- balls[0].radius)-(wall.pos.x+wall.length/2),0,0)
            springs.append(helix(pos=vector(wall.pos.x+wall.length/2,0,0),axis=displacement,radius=RADIUS,thickness=0.05,coils=10))
        elif i!=NUM_OSCILLATORS:
            balls.append(sphere(pos=vector(equilibrium_x + sim.getState()[i], 0, 0), radius=.3, color=dark_green))
            springs.append(helix(pos=vector(balls[i-1].pos.x+balls[i-1].radius,0,0),axis=vector((balls[i].pos.x -balls[i].radius)-(balls[i-1].pos.x+balls[i-1].radius),0,0),radius=RADIUS,thickness=0.05,coils=10))
        else:
            springs.append(helix(pos=vector(balls[i-1].pos.x+balls[i-1].radius,0,0),axis=vector(wall2.pos.x-(wall2.length/2)-(balls[i-1].pos.x+balls[i-1].radius),0,0),radius=RADIUS,thickness=0.05,coils=10))


    while True:
        rate(120)
        if running:
            for _ in range(10):
                sim.step()
            state=sim.getState()
            for i, ball in enumerate(balls):
                if i==0:
                    equilibrium_x = (i - (NUM_OSCILLATORS - 1)/2) * d
                    ball.pos.x=equilibrium_x+state[i]
                    springs[i].axis=vector((ball.pos.x-RADIUS)-(wall.pos.x+wall.length/2),0,0)
                    springs[i+1].pos.x=ball.pos.x+RADIUS
                elif i!=len(balls)-1:
                    equilibrium_x = (i - (NUM_OSCILLATORS - 1)/2) * d
                    ball.pos.x = equilibrium_x + state[i]
                    springs[i].axis=vector(balls[i].pos.x-RADIUS-springs[i].pos.x,0,0)
                    springs[i+1].pos.x=ball.pos.x+RADIUS
                else:
                    equilibrium_x = (i - (NUM_OSCILLATORS - 1)/2) * d
                    ball.pos.x=equilibrium_x+state[i]
                    springs[i].axis=vector(balls[i].pos.x-RADIUS-springs[i].pos.x,0,0)
                    springs[i+1].pos.x=ball.pos.x+RADIUS
                    springs[i+1].axis=vector(wall2.pos.x-(wall2.length/2)-springs[i+1].pos.x,0,0)
##update axis of current spring, update position of next spring.
def LorentzAttractorSimulation(sim):
    scene = canvas(
        title="Coupled Oscillators",width=1400,height=800,background=color.black)
    scene.center = vector(0, 0, 0)
    scene.range = 8
    scene.autoscale = False
    scene.forward = vector(0, 0, -2)
    initialState=sim.getState()
    particle=sphere(position=vector(initialState[0],initialState[1],initialState[2]),radius=1,make_trail=True,trail_radius=.1,trail_color=color.yellow,trail_type="curve",retain=1000,color=color.cyan)
    def handleEvent(evt):
        global running 
        if evt.key == ' ':
            running = not running
    scene.bind('keydown',handleEvent)
    counter=0
    while True:
        rate(120)
        if running:
            for _ in range(10):
                sim.step()
            state=sim.getState()
            particle.pos=vector(state[0],state[1],state[2])

def main():
    mass=np.array([1,1,1,1,1])
    k=np.array([3,3,3,3,3,3])
    A=OscillatorMatrix(mass,k)
    eig=np.linalg.eigvalsh(A[5:10,0:5])
    forces = [
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:0.0,
        lambda t:3*np.exp(-.5*t)*np.sin(np.sqrt(-eig[1])*t),
        lambda t:0.0,
    ]
    A=OscillatorMatrix(mass,k)
    propagator=partial(coupledOscillator,force=forces,A=A)
    LorentzPropagator=partial(lorentzAttractor,sigma=10,rho=28,beta=8/3)
    initialTime=0
    initialState=np.array([1,0,0])
    #initialState=np.concatenate([initialState,np.zeros(NUM_OSCILLATORS)])
    oscillatorSimulation=Simulation(initialTime,initialState,propagator)
    LorentzSimulation=Simulation(initialTime,initialState,LorentzPropagator)
    #vPythonOscillator(oscillatorSimulation)
    LorentzAttractorSimulation(LorentzSimulation)  
if __name__ == "__main__":
    main()
    


#make_trail=True,trail_radius=.05,trail_color=color.red,trail_type="curve",retain=500