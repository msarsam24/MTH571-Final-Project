'''This file will have a multitude of different functions f(t,y) corresonding to the time 
derivative of the state vector y '''
import numpy as np
from numpy.typing import NDArray


def coupledOscillator(t:float,y:NDArray[np.float64],force:NDArray[np.float64],A):

    '''Returns the function f(t,y) so the simulation can update y for RK4. '''

def OscillatorMatrix(m:NDArray[np.float64],k:NDArray[np.float64]):

    n=len(m)
    A=np.zeros((n,n))
    ##Initialize the first and last row of A manually 
    first=np.array([-1*(k[0]+k[1])/m[0],k[1]/m[0]])
    last=np.array([k[-2]/m[-1],-1*(k[-2]+k[-1])/m[-1]])
    A[n-1,n-2:n]=last
    A[0,0:2]=first
    for i in range(1,n-1):
        current=np.array([(k[i]/m[i]),-1*(k[i]+k[i+1])/m[i],(k[i+1]/m[i])])
        A[i,(i-1):(i+2)]=current
    return A