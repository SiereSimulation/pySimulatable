from ForceResult import ForceResult
from DoF import DoF
import numpy as np
import Material
from scipy.sparse import csr, csr_matrix

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
        self.internal_force = ForceResult()
        self.external_force = ForceResult()
        self.damping_force = ForceResult()
        self.mass = csr_matrix([0])
    def get_material(self) -> Material.Material:
        return self.material
    def get_dof(self) -> DoF:
        return self.dof
    def get_mass(self) -> csr_matrix:
        return self.mass
    def get_internal_force(self):
        return self.internal_force
    def get_external_force(self):
        return self.external_force
    def get_damping_force(self):
        return self.damping_force
    def update(self, simulator):
        # can do something to the object before simulation
        simulator.simulate(self)
        # can do something after
    def update_dof(self, positions, velocities):
        print(f'updating dof')
        self.dof.set_positions(positions)
        self.dof.set_velocities(velocities)
    def update_mesh(self):
        self.mesh.deform(self.dof.get_full_positions())
    def update_force_result(self):
        if(self.material.mtype == Material.FEMMaterial):
            self.force.calculate_force_result()
        elif():
            pass
        else:
            pass


class Environment(ISimulatable):

    def __init__(self):
        print(f'{type(self).__name__} created')
        self.simulatable_objects = []
        self.gravity = np.array([0,0,-9.8])     
        self.environment_simulator = None
        
    def add(self, simulatable):
        print(f'adding simulatable')
        self.simulatable_objects.append(simulatable)
    
    def set_gravity(self, gravity):
        self.gravity = gravity

    def request_frame(self):
        self.update(self.environment_simulator)
    def update(self, simulator):
        # can do something with the environment before simulation
        simulator.simulate(self)
        # can do something with the environment after simulation