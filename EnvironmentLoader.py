import Simulatable
import Simulator
import Mesh
import Material
from Material import ElasticityModel,FEMModelType, MaterialModel
import numpy as np
import pyredner
import pyvista as pv
import tetgen
import numpy as np
import json
import ForceSimulatorBuilder
import ForceCalculator
import ForceIntegrator

class EnvironmentLoader:
    def __init__(self):
        print(f'{type(self).__name__} created')
        self.environment = Simulatable.Environment()
        self.environment.environment_simulator = Simulator.EnvironmentSimulator()
        
    def load(self,filepath):
        print(f'loading {filepath}')

        with open(filepath) as f:
            data = json.load(f)
        
        mesh_param = data["simulatable_list"]["example_solid_object"]["mesh"]
        material_param = data["simulatable_list"]["example_solid_object"]["material"]
        integrator_param = data
        # pv_mesh = pv.read(mesh_param["source"])
        mesh = Mesh.Mesh()
        verts, elem = Mesh.Mesh.read_tetgen_file(mesh_param["source"]+".node", mesh_param["source"] +".ele")
        mesh.load_mesh(verts,elem)
        if material_param["FEM"]:
            elastisity_model = Material.ElasticityModel(material_param["elasticity_model"]["model"])
            density = material_param["density"]
            youngs = material_param["elasticity_model"]["youngs"]
            poisson = material_param["elasticity_model"]["poisson"]
            material = Material.FEMMaterial(density=density,youngs=youngs,poisson=poisson,mtype=elastisity_model,femtype=FEMModelType.CG)
            object1 = Simulatable.SolidObject(dimension=data["dimension"],material=material,mesh=mesh)
            force_calculator = ForceCalculator.FEMDiscretizationCalculator(object1)
        integrator_param = data["simulatable_list"]["example_solid_object"]["integrator"]
        if integrator_param == "SI":
            force_integrator = ForceIntegrator.SemiImplicitIntegrator()
        force_simulator_builder_1 = ForceSimulatorBuilder.ForceSimulatorBuilder()
        force_simulator_builder_1.set_force_calculator(force_calculator)
        force_simulator_builder_1.set_force_integrator(force_integrator)
        force_simulator = force_simulator_builder_1.build()

        # # object2 = Simulatable.SolidObject(material=material,mesh=mesh)

        simulatables = []
        simulatables.append(object1)
        


        # # simulatables.append(object2)
        # for simulatable in simulatables:
        #     self.environment.add(simulatable)
        self.environment.add(object1)
        simulator = Simulator.ForceSimulator()
        simulator.add(force_simulator)
        # contact = Simulator.ContactSimulator()
        # simulator.add(integrator)
        # simulator.add(contact)
        self.environment.environment_simulator.simulator_map = {simulator: simulatables}
        gravity = np.array([0,0,-9.8])     
        self.environment.set_gravity(gravity)
        print(f'end loading {filepath}')
        return self.environment

