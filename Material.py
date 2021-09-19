from enum import Enum

class MaterialType(Enum):
    neohookean = 1
    stable_neohookean = 2
    stvk = 3
    linear = 4
    arap = 5

class Material:
    def __init__(self,density) -> None:
        print(f'{type(self).__name__} created')
        self.density = density

class FEMMaterial(Material):
    def __init__(self, density, youngs, poisson, mtype) -> None:
        super().__init__(density)
        print(f'{type(self).__name__} created')
        self.youngs = youngs
        self.poisson = poisson
        self.mtype = mtype
class MassSpringMaterial:
    def __init__(self, density, stiffness) -> None:
        super().__init__(density)
        print(f'{type(self).__name__} created')
        self.stiffness = stiffness
