from enum import Enum
from Damping import Damping


class MaterialModel(Enum):
    FEM = 1
    MassSpring = 2
    
class ElasticityModel(Enum):
    neohookean = 1
    stable_neohookean = 2
    stvk = 3
    linear = 4
    arap = 5

class FEMModelType(Enum):
    CG = 1
    DG = 2

class Material:
    def __init__(self,material_model: MaterialModel, density) -> None:
        print(f'{type(self).__name__} created')
        self.density = density
        self.material_model = material_model
        self.damping_model = Damping()
    

class FEMMaterial(Material):
    def __init__(self, density, youngs, poisson, mtype: ElasticityModel, material_model: MaterialModel = MaterialModel.FEM, femtype : FEMModelType = FEMModelType.CG) -> None:
        super().__init__(material_model,density)
        print(f'{type(self).__name__} created')
        self.youngs = youngs
        self.poisson = poisson
        self.mtype = mtype
        self.femtype = femtype
class MassSpringMaterial:
    def __init__(self,material_model, density, stiffness) -> None:
        super().__init__(material_model,density)
        print(f'{type(self).__name__} created')
        self.stiffness = stiffness
