from ForceResult import ForceResult
from abc import ABC, abstractmethod
from Simulatable import SolidObject
import numpy as np
from scipy.sparse import csc_matrix

class IDiscretizationCalculator(ABC):
    def __init__(self,simulatable) -> None:
        print(f'{type(self).__name__} created')
        self.simulatable = simulatable
    def calculate(self) -> None:
        pass

class FEMDiscretizationCalculator(IDiscretizationCalculator):
    Iv = np.eye(3) # Identity for vector
    G = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]])
    dimension = 3
    def __init__(self,solid_object: SolidObject) -> None:
        print(f'{type(self).__name__} created')
        self.solid_object = solid_object
        self.mesh = solid_object.get_mesh()
        elements = self.mesh.elements
        self.Dm = np.empty((self.dimension * elements.shape[0], self.dimension)) # reference shape matrix
        self.DmINV = np.empty((self.dimension * elements.shape[0], self.dimension)) # inverse reference shape matrix
        self.W = np.empty((elements.shape[0],1)) # undefromed volume
        self.T = np.empty((9 * elements.shape[0], 12)) # transformation matrix from deformation to deformation gradient
        self.M = np.empty((self.dimension * self.mesh.vertices.shape[0],self.dimension * self.mesh.vertices.shape[0]))
        self.F = np.empty((self.dimension * elements.shape[0], self.dimension))
        self.FINV = np.empty((self.dimension * elements.shape[0], self.dimension))
        self.initialize_FEM_discretization()
    
    def initialize_FEM_discretization(self):
        print(f'initializing FEM mesh')
        for element_index in range(self.mesh.elements.shape[0]):
            element_node = self.mesh.undeformed_vertices[self.mesh.elements[element_index,:]]
            self.initialize_reference_shape_matrix_and_transform(element_index,element_node)
            self.initialize_volume_and_mass(element_index,element_node)
            self.initialize_stiffness_matrix_indices(element_index,element_node)

    def initialize_volume_and_mass(self,element_index,element_node):
        self.W[element_index] = np.abs(np.linalg.det(element_node.transpose().dot(self.G)))
        for element in self.mesh.elements[element_index,:]:
            for mass_matrix_index in range(element*3, (element+1)*3):
                self.M[mass_matrix_index,mass_matrix_index] = self.M[mass_matrix_index,mass_matrix_index] + self.solid_object.get_material().density*self.W[element_index]/4
                
    def initialize_reference_shape_matrix_and_transform(self,element_index,element_node):
        # print(f'initializing discrete gradient (Dm and DmINV) and transform (T) for a FEM mesh')
        self.Dm[3 * element_index : 3 * (element_index + 1), : ] = element_node.transpose().dot(self.G)
        if(element_index == 111):
            test = 1
        self.DmINV[3 * element_index : 3 * (element_index + 1), : ] = np.linalg.inv(element_node.transpose().dot(self.G))
        self.T[9*element_index:9*(element_index+1),:] = np.kron((self.G.dot(self.DmINV[3 * element_index : 3 * (element_index + 1), : ])).transpose(), self.Iv )

    def initialize_stiffness_matrix_indices(self,element_index,element_node):
        # print(f'initializing stiffness matrix (ii,jj) for a FEM mesh')
        self.ii = np.array([])
        self.jj = np.array([])

    def calculate_deformation_gradient(self):
        print(f'calculating deformation gradient F for a FEM mesh')
    def calculate(self):
        self.mesh.deform(self.solid_object.get_dof().get_full_positions())
        self.calculate_deformation_gradient()
        print(f'calculating discretized quantities (forces, force grad, etc')
        energy = 0
        force = np.array([0])
        force_gradient = csc_matrix([0])
        self.solid_object.internal_force.set_energy(energy)
        self.solid_object.internal_force.set_force(force)
        self.solid_object.internal_force.set_force_gradient(force_gradient)

        

    
        


