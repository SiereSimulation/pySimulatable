import numpy as np
import Material
import Mesh
from scipy.sparse import csr_matrix

class ForceResult:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
        self.energy = 0
        self.force = np.array([0])
        self.force_gradient = csr_matrix([0])
    def get_energy(self):
        return self.energy
    def get_force(self) -> np.array:
        return self.force
    def get_force_gradient(self) -> np.array:
        return self.force_gradient
    def calculate_force_result(self, material: Material.Material, mesh: Mesh.Mesh):
        print(f'calculating fem force result')
        elements = mesh.get_elements()
        for i_element in range(elements.size):
            if material.material_model == Material.MaterialModel.FEM:
                if material.femtype == Material.FEMModelType.CG:
                    if material.mtype == Material.FEMMaterialType.neohookean:
                        pass
                    elif material.mtype == Material.FEMMaterialType.stable_neohookean:
                        pass
                    elif material.mtype == Material.FEMMaterialType.stvk:
                        pass
                    elif material.mtype == Material.FEMMaterialType.linear:
                        pass
                    elif material.mtype == Material.FEMMaterialType.arap:
                        pass
                    else:
                        pass
                elif material.femtype == Material.FEMModelType.DG:
                    pass
                else:
                    pass
            elif material.material_model == Material.MaterialModel.MassSpring:
                pass

