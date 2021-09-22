import Simulator
import DiscretizationCalculator
import ForceIntegrator
import Simulator

class ForceSimulatorBuilder:
    def __init__(self) -> None:
        self.force_simulator = Simulator.ForceSimulator()
    def build(self) -> Simulator.ISimulator:
        return self.force_simulator

    def set_discretization_calculator(self, discretization_calculator: DiscretizationCalculator.IDiscretizationCalculator):
        self.force_simulator.set_discretization_calculator(discretization_calculator)
        
    def set_force_integrator(self, force_integrator: ForceIntegrator.IForceIntegrator):
        self.force_simulator.set_force_integrator(force_integrator)
    