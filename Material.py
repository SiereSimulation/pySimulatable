from enum import Enum
from Damping import Damping
import numpy as np

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
    def __init__(self,material_model: MaterialModel = MaterialModel.FEM , density : float = 1000 ) -> None:
        print(f'{type(self).__name__} created')
        self.density = density
        self.material_model = material_model
        self.damping_model = Damping()
    

class FEMMaterial(Material):
    def __init__(self, density, youngs, poisson, mtype, material_model: MaterialModel = MaterialModel.FEM, femtype : FEMModelType = FEMModelType.CG) -> None:
        super().__init__(material_model,density)
        print(f'{type(self).__name__} created')
        self.femtype = femtype
        if type(youngs) is list:
            self.youngs = np.array(youngs)
            self.poisson = np.array(poisson)
            self.mtype = np.array(mtype)
            self.mu = self.youngs/(2*(1+self.poisson))
            self.lambd = (self.youngs * self.poisson)/((1+self.poisson)*(1-2*self.poisson))
            self.density = np.array(density)
        else:
            self.youngs = youngs
            self.poisson = poisson
            self.mtype = mtype
            self.mu = youngs/(2*(1+poisson))
            self.lambd = (youngs * poisson)/((1+poisson)*(1-2*poisson))
            self.density = density

            
class MassSpringMaterial:
    def __init__(self,material_model, density, stiffness) -> None:
        super().__init__(material_model,density)
        print(f'{type(self).__name__} created')
        self.stiffness = stiffness
