from Simulatable import ISimulatable, SolidObject
import numpy as np
from numpy.core.fromnumeric import transpose
import scipy.sparse
from scipy.sparse.linalg import spsolve, eigs
import ForceCalculator
import ForceIntegrator

class ISimulator:
    def __init__(self):
        print(f'{type(self).__name__} created')
    def simulate(self, simulatable):
        pass

class ForceSimulator(ISimulator):
    def __init__(self):
        super().__init__()
        self.simulators = []
        self.step_size = 5e-3
    def add(self, simulator):
        self.simulators.append(simulator)
    def simulate(self, simulatable:ISimulatable):
        if not self.simulators:
            self.force_calculator.calculate()
            self.force_integrator.integrate(self.step_size, simulatable.get_dof(), simulatable.internal_force, simulatable.external_force, simulatable.damping_force,simulatable.get_mass())
        else:
            for simulator in self.simulators:
                simulator.simulate(simulatable) 
    def set_step_size(self, step_size):
        self.step_size = step_size
    def set_force_calculator(self,force_calculator: ForceCalculator.IForceCalculator):
        self.force_calculator = force_calculator
    def set_force_integrator(self,force_integrator: ForceIntegrator.IForceIntegrator):
        self.force_integrator = force_integrator


        

class EnvironmentSimulator(ISimulator):
    def __init__(self):
        pass
    def simulate(self, environment):
        
        # can simulate the environment first, for example gravity, wind etc
        environment.calculate_gravity()
        # simulate indiviual objects in the environment
        for simulator in self.simulator_map:
            simulatable_list = self.simulator_map[simulator]
            for simulatable in simulatable_list:
                simulatable.update(simulator)
        environment.collision_detection()
        environment.contact_resolution()