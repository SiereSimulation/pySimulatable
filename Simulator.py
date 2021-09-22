from Simulatable import ISimulatable, SolidObject
import numpy as np
from numpy.core.fromnumeric import transpose
import scipy.sparse
from scipy.sparse.linalg import spsolve, eigs
import DiscretizationCalculator
import ForceIntegrator

class ISimulator:
    def __init__(self):
        print(f'{type(self).__name__} created')
    def simulate(self, simulatable):
        pass
class MovementSimulator(ISimulator):
    def __init__(self):
        super().__init__()
        self.simulators = []
    def add(self, simulator):
        self.simulators.append(simulator)
    def simulate(self, simulatable):
        for simulator in self.simulators:
            simulator.simulate(simulatable) 

class ForceSimulator(ISimulator):
    def __init__(self):
        super().__init__()
    def simulate(self, simulatable:ISimulatable):
        self.discretization_calculator.calculate()
        self.force_integrator.integrate(1e-3, simulatable)
    def set_discretization_calculator(self,discretization_calculator: DiscretizationCalculator.IDiscretizationCalculator):
        self.discretization_calculator = discretization_calculator
    def set_force_integrator(self,force_integrator: ForceIntegrator.IForceIntegrator):
        self.force_integrator = force_integrator

class ContactSimulator(ISimulator):
    def simulate(self, solid_object):
        super().__init__()
        print(f'running contact simulator')
        

class SIEREIntegrator(ISimulator):
    def __init__(self, subspace_dimension):
        super().__init__()
        self.subspace_dimension = subspace_dimension
    
    @staticmethod
    def phi(matrix):
        print(f'calculating phi')

    def simulate(self, solid_object):
        
        # get current dof and mass of the object
        dof = solid_object.get_dof()
        positions = dof.get_positions()
        velocities = dof.get_velocities()
        dof_size = positions.size
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
        dt = self.step_size
        total_force = external_force + internal_force + damping_force
        
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
    def simulate(self, environment):
        
        # can simulate the environment first, for example gravity, wind

        # simulate indiviual objects in the environment
        for simulator in self.simulator_map:
            simulatable_list = self.simulator_map[simulator]
            for simulatable in simulatable_list:
                simulatable.update(simulator)