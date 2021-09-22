from Simulatable import SolidObject
import numpy as np
from numpy.core.fromnumeric import transpose
import scipy.sparse
from scipy.sparse.linalg import spsolve, eigs

class IForceIntegrator:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
        pass
    def integrate(self, step_size, simulatable):
        pass

class SemiImplicitIntegrator(IForceIntegrator):
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
        super().__init__()
    def integrate(self, step_size, solid_object: SolidObject):
        print(f'running semi implicit integrator')
        # get current dof and mass of the object
        dof = solid_object.get_dof()
        positions = dof.get_positions()
        velocities = dof.get_velocities()
        mass_matrix = solid_object.get_mass()
        
        # get current forces
        internal_force_result = solid_object.get_internal_force()
        internal_force = internal_force_result.get_force()
        stiffness_matrix = -internal_force_result.get_force_gradient()
        external_force_result = solid_object.get_external_force()
        external_force = external_force_result.get_force()
        damping_force_result = solid_object.get_damping_force()
        damping_force = damping_force_result.get_force()
        damping_matrix = -damping_force_result.get_force_gradient()

        # construct properties only needed inside the simulator
        dt = step_size
        total_force = external_force + internal_force + damping_force
        
        # solve the equation
        A = mass_matrix - dt * damping_matrix + (dt**2) * stiffness_matrix
        b = dt * (total_force - dt * stiffness_matrix * velocities)
        delta_velocities = spsolve(A,b)
        
        # update the object using the result
        new_velociteis = velocities + delta_velocities
        new_positions = positions + dt * new_velociteis

        solid_object.update_dof(new_positions, new_velociteis)
