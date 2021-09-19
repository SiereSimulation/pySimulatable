import numpy as np

class Mesh:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
    def load_mesh(self, vertices, elements) -> None:
        self.undeformed_vertices = vertices
        self.vertices = vertices
        self.elements = elements
    def deform(self,deformation,indices):
        print(f'deforming a mesh')
        self.vertices[indices] = self.undeformed_vertices + deformation

class FEMMesh(Mesh):
    def __init__(self) -> None:
        super().__init__()
        print(f'{type(self).__name__} created')
    def load_mesh(self, vertices, elements) -> None:
        super().load_mesh(vertices, elements)
        self.initialize_deformation_gradient_transform()
        self.initialize_discrete_gradient()
        self.initialize_volume()
        self.initialize_stiffness_matrix_indices() 
        self.calculate_deformation_gradient()
    def deform(self, deformation, indices = np.array([0])):
        super().deform(deformation, indices)
        self.calculate_deformation_gradient()

    def initialize_volume(self):
        self.volume = np.array([])
        print(f'initializing volume for a FEM mesh')
    def initialize_discrete_gradient(self):
        print(f'initializing discrete gradient (Dm and DmINV) for a FEM mesh')
        self.discrete_gradient = np.array([])
        self.inv_discrete_gradient = np.array([])
    def initialize_deformation_gradient_transform(self):
        print(f'initializing deformation gradient transform (T) for a FEM mesh')
        self.deformation_gradient_transform = np.array([])
    def initialize_stiffness_matrix_indices(self):
        print(f'initializing stiffness matrix (ii,jj) for a FEM mesh')
        self.ii = np.array([])
        self.jj = np.array([])
    def calculate_deformation_gradient(self):
        print(f'calculating deformation gradient F for a FEM mesh')
        self.deformation_gradient = np.array([])
        self.inv_deformation_gradient = np.array([])
