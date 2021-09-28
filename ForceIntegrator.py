from DoF import DoF
from ForceResult import ForceResult
from Simulatable import SolidObject
import numpy as np
from numpy.core.fromnumeric import transpose
import scipy.sparse
from scipy.sparse.linalg import spsolve, eigs
from scipy.sparse import csc_matrix
import math
class IForceIntegrator:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
        pass
    def integrate(self, step_size):
        pass

class SemiImplicitIntegrator(IForceIntegrator):
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
        super().__init__()
    def integrate(self, step_size, dof:DoF, internal_force_result: ForceResult, external_force_result: ForceResult, damping_force_result:ForceResult, mass_matrix: csc_matrix):
        print(f'running semi implicit integrator')
        # get current dof and mass of the object
        positions = dof.get_positions()
        velocities = dof.get_velocities()
        
        # get current forces
        internal_force = internal_force_result.get_force()
        stiffness_matrix = -internal_force_result.get_force_gradient()
        external_force = external_force_result.get_force()
        damping_force = damping_force_result.get_force()
        damping_matrix = -damping_force_result.get_force_gradient()

        # construct properties only needed inside the simulator
        dt = step_size
        total_force = external_force + internal_force + damping_force
        
        # solve the equation
        A = mass_matrix - dt * damping_matrix + (dt**2) * stiffness_matrix
        b = dt * (total_force - dt * stiffness_matrix * dof.get_full_velocities())
        delta_velocities = spsolve(A[dof.free_indices][:,dof.free_indices],b[dof.free_indices])
        
        # update the object using the result
        new_velociteis = velocities + delta_velocities
        new_positions = positions + dt * new_velociteis

        dof.set_positions(new_positions)
        dof.set_velocities(new_velociteis)


