class Simulation:
    h=1/1200 ##Step size for the simulation
    def __init__(self,time,state,propagator):
        self.time=time
        self.state=state
        self.propagator=propagator
    
    def step(self):
        '''RK4 implementation'''
        k1=self.h*(self.propagator(self.time,self.state))
        k2=self.h*(self.propagator(self.time+self.h/2,self.state+ k1/2))
        k3=self.h*(self.propagator(self.time+self.h/2,self.state+k2/2))
        k4=self.h*(self.propagator(self.time+self.h,self.state+k3))
        self.state=self.state+ (1/6)*(k1+2*k2+2*k3+k4)
        self.time+=self.h
    def getState(self):
        return self.state