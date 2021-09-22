import numpy as np
import Material
import Mesh
from scipy.sparse import csc_matrix

class ForceResult:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
        self.energy = 0
        self.force = np.array([0])
        self.force_gradient = csc_matrix([0])
    def get_energy(self) -> float:
        return self.energy
    def get_force(self) -> np.array:
        return self.force
    def get_force_gradient(self) -> csc_matrix:
        return self.force_gradient
    def set_energy(self,energy: float):
        self.energy = energy
    def set_force(self, force: np.array):
        self.force = force
    def set_force_gradient(self, force_gradient: csc_matrix):
        self.force_gradient = force_gradient
