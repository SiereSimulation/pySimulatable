import Simulator
import ForceCalculator
import ForceIntegrator
import Simulator

class ForceSimulatorBuilder:
    def __init__(self) -> None:
        self.force_simulator = Simulator.ForceSimulator()
    def build(self) -> Simulator.ISimulator:
        return self.force_simulator

    def set_force_calculator(self, force_calculator: ForceCalculator.IForceCalculator):
        self.force_simulator.set_force_calculator(force_calculator)
        
    def set_force_integrator(self, force_integrator: ForceIntegrator.IForceIntegrator):
        self.force_simulator.set_force_integrator(force_integrator)
    