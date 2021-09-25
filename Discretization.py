import numpy as np
from scipy.sparse.csc import csc_matrix


class Discretization:
    def __init__(self) -> None:
        pass
    def initialize_discretization(self):
        pass


class FEMDiscretization(Discretization):
    def __init__(self,dimension,mesh,material) -> None:
        print(f'{type(self).__name__} created')
        self.Dm = np.empty((dimension * mesh.elements.shape[0], dimension)) # reference shape matrix
        self.Ds = np.empty((dimension * mesh.elements.shape[0], dimension)) # reference shape matrix
        self.DmINV = np.empty((dimension * mesh.elements.shape[0], dimension)) # inverse reference shape matrix
        self.W = np.empty((mesh.elements.shape[0],1)) # undefromed volume
        self.T = np.empty((9 * mesh.elements.shape[0], 12)) # transformation matrix from deformation to deformation gradient
        self.M = csc_matrix((dimension * mesh.vertices.shape[0],dimension * mesh.vertices.shape[0]))
        self.F = np.empty((dimension * mesh.elements.shape[0], dimension))
        self.FINV = np.empty((dimension * mesh.elements.shape[0], dimension))
        self.stiffness_matrix_index_count = 0
        self.ii = np.empty(mesh.elements.shape[0] * 144)
        self.jj = np.empty(mesh.elements.shape[0] * 144)
        self.density = material.density
        self.mu = material.mu
        self.lambd = material.lambd
        self.mtype = material.mtype
        
