import numpy as np
from numpy.core.fromnumeric import transpose
import scipy.sparse
from scipy.sparse.linalg import spsolve, eigs


class ISimulator:
    def __init__(self):
        print(f'{type(self).__name__} created')
    def simulate(self, simulatable):
        pass
class MovementSimulator(ISimulator):
    def __init__(self):
        self.simulators = []
    def add(self, simulator):
        self.simulators.append(simulator) 
class SemiImplicitIntegrator(ISimulator):
    def simulate(self, solid_object):
        
        # get material parameters needed for the simulator
        material =solid_object.get_material()
        damping_alpha = material.damping_alpha
        damping_beta = material.damping_beta

        # get current dof and mass of the object
        dof = solid_object.get_dof()
        positions = dof.get_positions()
        velocities = dof.get_velocities()
        mass_matrix = solid_object.get_mass()
        
        # get current force state
        force = solid_object.get_force_state()
        internal_force = force.get_internal()
        stiffness_matrix = -force.get_gradient()
        external_force = force.get_external()

        # construct properties only needed inside the simulator
        dt = self.step_size()
        damping_matrix = - damping_alpha * mass_matrix - damping_beta * stiffness_matrix
        total_force = external_force + internal_force + damping_matrix * velocities
        
        # solve the equation
        A = mass_matrix - dt * damping_matrix + (dt**2) * stiffness_matrix
        b = dt * (total_force - dt * stiffness_matrix * velocities)
        delta_velocities = spsolve(A,b)
        
        # update the object using the result
        new_velociteis = velocities + delta_velocities
        new_positions = positions + dt * new_velociteis

        solid_object.update_dof(new_positions, new_velociteis)



class SIEREIntegrator(ISimulator):
    def __init__(self, subspace_dimension):
        super().__init__()
        self.subspace_dimension = subspace_dimension
    
    @staticmethod
    def phi(matrix):
        print(f'calculating phi')

    def simulate(self, solid_object):
        
        # get material parameters needed for the simulator
        material =solid_object.get_material()
        damping_alpha = material.damping_alpha
        damping_beta = material.damping_beta

        # get current dof and mass of the object
        dof = solid_object.get_dof()
        positions = dof.get_positions()
        velocities = dof.get_velocities()
        mass_matrix = solid_object.get_mass()
        dof_size = dof.get_size()
        
        # get current force state
        force = solid_object.get_force_state()
        internal_force = force.get_internal()
        stiffness_matrix = -force.get_gradient()
        external_force = force.get_external()

        # construct properties only needed inside the simulator
        dt = self.step_size()
        damping_matrix = - damping_alpha * mass_matrix - damping_beta * stiffness_matrix
        total_force = external_force + internal_force + damping_matrix * velocities
        
        [Us, D] = eigs(stiffness_matrix, mass_matrix, self.subspace_dimension,'smallestabs')
        vG = Us.dot(Us.transpose()).dot(mass_matrix).dot(velocities)
        vH = velocities - vG
        fG = mass_matrix.dot(Us).dot(Us.transpose()).dot(total_force)
        fH = total_force - fG
        H = np.array([vH], [spsolve(mass_matrix,fH)])

        JGr = np.array([np.zeros((self.subspace_dimension,self.subspace_dimension)), np.ones((self.subspace_dimension,self.subspace_dimension))], [-D, np.zeros((self.subspace_dimension,self.subspace_dimension))])
        Gr = np.array([Us.transpose().dot(mass_matrix).dot(velocities)], [Us.transpose().dot(total_force)])

        p = self.phi(dt * JGr)

        delta = dt*H + dt * np.array([Us, np.zeros((dof_size,self.subspace_dimension))], [np.zeros((dof_size,self.subspace_dimension)), Us]).dot(p).dot(Gr)

        J = np.array([np.zeros(dof_size), scipy.sparse.eye(dof_size)], [-spsolve(mass_matrix,stiffness_matrix), np.zeros(dof_size)])
        JG = np.array([np.zeros(dof_size), Us.dot(Us.transpose()).dot(mass_matrix)], [-Us.dot(Us.transpose()).dot(stiffness_matrix).dot(Us).dot(Us.transpose).dot(mass_matrix), np.zeros(dof_size)])
        JH = J - JG
        x0 = spsolve(scipy.sparse.eye(2*dof_size) - dt* JH, delta)


        
        # update the object using the result
        delta_positions, delta_velocities = np.split(x0,2)
        new_positions = positions + delta_positions
        new_velociteis = velocities + delta_velocities

        solid_object.update_dof(new_positions, new_velociteis)


        

class EnvironmentSimulator(ISimulator):
    def __init__(self):
        
        pass