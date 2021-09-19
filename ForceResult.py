import numpy as np
import Material
import Mesh


class ForceResult:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
    def get_internal(self) -> np.array:
        return self.internal_force
    def get_external(self) -> np.array:
        return self.external_force
    def get_gradient(self) -> np.array:
        return self.force_gradient
    def calculate_fem_force_result(self, material: Material.FEMMaterial, mesh: Material.FEMMesh):
        print(f'calculating fem force result')
        elements = mesh.get_elements()
        for i_element in range(elements.size):
            if material.mtype == Material.MaterialType.neohookean:
                pass
            elif material.mtype == Material.MaterialType.stable_neohookean:
                pass
            elif material.mtype == Material.MaterialType.stvk:
                pass
            elif material.mtype == Material.MaterialType.linear:
                pass
            elif material.mtype == Material.MaterialType.arap:
                pass
        
    def calculate_mass_spring_force_result(self, material: Material.MassSpringMaterial, mesh: Mesh):
        print(f'calculating mass spring force result')
        elements = mesh.get_elements()
        for i_element in range(elements.size):
            material.stiffness[i_element]
