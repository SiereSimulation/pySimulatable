from ForceResult import ForceResult
from DoF import DoF
import numpy as np

class ISimulatable:
    def __init__(self):
        print(f'{type(self).__name__} created')
    def update(self,simulator):
        simulator.simulate()


class SolidObject(ISimulatable):
    def __init__(self,material,mesh):
        super().__init__()
        print(f'{type(self).__name__} created')
        self.material = material
        self.mesh = mesh
        self.dof = DoF()
        self.force = ForceResult()
    def update_dof(self, positions, velocities):
        print(f'updating dof')
        self.mesh.deform(positions)
        self.force.calculate_fem_force_result()


class Environment(ISimulatable):
    def __init__(self):
        print(f'{type(self).__name__} created')
        self.simulatable_objects = []
        self.gravity = np.array([0,0,-9.8])     
        self.environment_simulator = []
        
    def add(self, simulatable):
        print(f'adding simulatable')
        self.simulatable_objects.append(simulatable)
    
    def set_gravity(self, gravity):
        self.gravity = gravity

    def update(self, simulator=None):
        if simulator == None:
            self.update(self.environment_simulator)
        else:
            pass
