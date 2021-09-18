import pySimulatable
import numpy as np

if __name__ == "__main__":
    draw_frame = True
    env = EnvironmentLoader()
    env.load("env file")

    num_frames = 100

    for i in range(num_frames):
        # env.update()
        if draw_frame:
            env.draw()


class EnvironmentLoader:
    def __init__(self):
        print(f'{type(self).__name__} created')
        self.environment = Environment()
    def load(self,filename):
        print(f'loading {filename}')
                
class ISimulatable:

    def update(self,simulator):
        pass


class Environment(ISimulatable):

    def __inti__(self):
        print(f'{type(self).__name__} created')
        self.simulatable_objects = []
        self.gravity = np.array(0,0,-9.8])     
        self.environment_simulator = []
        
    def add(self, simulatable):
        simulatable_objects.append(simulatable)
    
    def update(self, simulator=None):
        if simulator == None:
            self.update(self.environment_simulator)
        else:
            pass

class MovementSimulator(ISimulatable):
    def __init__(self):
        self.simulators = []
    def add(self, simulator):
        self.simulators.append(simulator) 

class Integrator(ISimulator):
    def simulate():
        pass

class ISimulator:
    def simulate(self, simulatable):
        pass

class EnvironmentSimulator(ISimulator):
    def __init__(self):
        self.simulator_map = {}