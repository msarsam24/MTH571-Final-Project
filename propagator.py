'''This file will have a multitude of different functions f(t,y) corresonding to the time 
derivative of the state vector y '''
import numpy as np
from numpy.typing import NDArray


def coupledOscillator(t:float,y:NDArray[np.float64],force:NDArray[np.float64],A):

    '''Returns the function f(t,y) so the simulation can update y for RK4. '''
    F = np.array([f(t) for f in force])
    return A@y + F
def OscillatorMatrix(m:NDArray[np.float64],k:NDArray[np.float64]):

    n=len(m)
    B=np.zeros((n,n))
    ##Initialize the first and last row of A manually 
    first=np.array([-1*(k[0]+k[1])/m[0],k[1]/m[0]])
    last=np.array([k[-2]/m[-1],-1*(k[-2]+k[-1])/m[-1]])
    B[n-1,n-2:n]=last
    B[0,0:2]=first
    for i in range(1,n-1):
        current=np.array([(k[i]/m[i]),-1*(k[i]+k[i+1])/m[i],(k[i+1]/m[i])])
        B[i,(i-1):(i+2)]=current
    A= np.block([
    [np.zeros((n, n)), np.eye(n)],
    [B, np.zeros((n, n))]])
    return A

def predatorPrey(t,y,alpha,beta,delta,gamma):
    '''Return predatorPrey f(t,y). '''
    xprime=alpha*y[0]-beta*y[0]*y[1]
    yprime=delta*y[0]*y[1]-gamma*y[1]
    return np.array([xprime,yprime])

def lorentzAttractor(t,y,sigma,rho,beta):
    x1=y[0]
    y1=y[1]
    z1=y[2]
    xdot=sigma*(y1-x1)
    ydot=x1*(rho-z1)-y1
    zdot=x1*y1-(beta*z1)
    return np.array([xdot,ydot,zdot])
    
