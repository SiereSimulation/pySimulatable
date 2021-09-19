import Simulatable
import Simulator
import Mesh
import Material
from Material import MaterialType
import numpy as np


class EnvironmentLoader:
    def __init__(self):
        print(f'{type(self).__name__} created')
        self.environment = Simulatable.Environment()
        self.environment_simulator = Simulator.EnvironmentSimulator()
        
    def load(self,filename):
        print(f'loading {filename}')

        mesh = Mesh.FEMMesh()
        material = Material.FEMMaterial(density=1,youngs=1e5,poisson=0.45,mtype=MaterialType.neohookean)

        object1 = Simulatable.SolidObject(material=material,mesh=mesh)
        object2 = Simulatable.SolidObject(material=material,mesh=mesh)

        simulatables = []
        simulatables.append(object1)
        simulatables.append(object2)
        for simulatable in simulatables:
            self.environment.add(simulatable)
        
        simulator = Simulator.SemiImplicitIntegrator()

        self.environment_simulator.simulator_map = {simulator: simulatables}
        gravity = np.array([0,0,-9.8])     
        self.environment.set_gravity(gravity)
        print(f'end loading {filename}')

