import numpy as np
from numpy.lib.arraysetops import unique

class Mesh:
    def __init__(self) -> None:
        print(f'{type(self).__name__} created')
    def load_mesh(self, vertices, elements) -> None:
        self.undeformed_vertices = vertices
        self.vertices = vertices
        self.elements = elements
    def deform(self,deformation):
        print(f'deforming a mesh')
        # can potentially change the vertices avoid reshaping/restructing the vertices and dofs
        # if deformation.shape == 1:
        #     deformation.reshape((3,-1))
        #     deformation = deformation.transpose()
        self.vertices = self.undeformed_vertices + deformation

    @staticmethod
    def read_tetgen_file(node_file, ele_file):
        with open(node_file, 'r') as f:
            lines = f.readlines()
            lines = [l.strip().split() for l in lines]
            vert_num = int(lines[0][0])
            verts = np.array([[float(v) for v in lines[i + 1][1:4]] for i in range(vert_num)])

        with open(ele_file, 'r') as f:
            lines = f.readlines()
            lines = [l.strip().split() for l in lines]
            ele_num = int(lines[0][0])
            elements = np.asarray([[int(e) for e in lines[i + 1][1:5]] for i in range(ele_num)], dtype=int) 
            if np.min(elements) == 1:
                elements = elements - 1
        return verts, elements

    @staticmethod
    def surface_triangulation(node, element):
        # translated from matlab distmesh by Per-Olof Persson
        faces = np.vstack([element[:,[0,1,2]], element[:,[0,1,3]], element[:,[0,2,3]], element[:,[1,2,3]]])
        node4 = np.array([element[:,3], element[:,2], element[:,1], element[:,0]]).flatten()
        faces = np.sort(faces, axis = 1)
        uni, index, reverse, counts = np.unique(faces,return_index=True, return_inverse=True, return_counts=True, axis=0)
        none_repeating_indices = index[counts==1]
        surface_triangulation = faces[none_repeating_indices,:]
        node4 = node4[none_repeating_indices]

        # ensure consistent orientation
        v0 = node[surface_triangulation[:,1],:] - node[surface_triangulation[:,0],:]
        v1 = node[surface_triangulation[:,2],:] - node[surface_triangulation[:,0],:]
        v2 = node[node4,:] - node[surface_triangulation[:,0],:]
        flip_index=np.nonzero(np.sum(np.cross(v0,v1,axis=1)*v2,1)>0)[0]
        surface_triangulation[np.ix_(flip_index,[1,2])] = surface_triangulation[np.ix_(flip_index,[2,1])]
        return surface_triangulation

# class FEMMesh(Mesh):
#     Iv = np.eye(3) # Identity for vector
#     G = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]])
#     def __init__(self) -> None:
#         super().__init__(3)
#         print(f'{type(self).__name__} created')
        
#     def load_mesh(self, vertices, elements) -> None:
#         super().load_mesh(vertices, elements)
#         self.Dm = np.empty((self.dimension * elements.shape[0], self.dimension)) # reference shape matrix
#         self.DmINV = np.empty((self.dimension * elements.shape[0], self.dimension)) # inverse reference shape matrix
#         self.W = np.empty((elements.shape[0],1)) # undefromed volume
#         self.T = np.empty((9 * elements.shape[0], 12)) # transformation matrix from deformation to deformation gradient
#         self.M = np.empty((self.dimension * vertices.shape[0],self.dimension * vertices.shape[0]))
#         action_list = []
#         # action_list.append(self.initialize_deformation_gradient_transform)
#         action_list.append(self.initialize_reference_shape_matrix)
#         action_list.append(self.initialize_deformation_gradient_transform)
#         action_list.append(self.initialize_volume)
#         action_list.append(self.initialize_mass)
#         self.elemental_calculation(action_list)
#         # self.initialize_deformation_gradient_transform()
#         # self.initialize_discrete_gradient()
#         # self.initialize_volume()
#         # self.initialize_stiffness_matrix_indices() 
#         # self.calculate_deformation_gradient()
#     def deform(self, deformation, indices = np.array([0])):
#         super().deform(deformation, indices)
        # self.calculate_deformation_gradient()

    # def initialize_volume(self,element_index,element_node):
    #     self.W[element_index] = np.abs(np.linalg.det(element_node.transpose().dot(self.G)))
    #     print(f'initializing volume for a FEM mesh')
    # def initialize_mass(self, element_index, element_node):
    #     print(f'initializing mass for a FEM mesh')
    #     for element in self.elements[element_index,:]:
    #         for mass_matrix_index in range(element*3, (element+1)*3):
    #             self.M[mass_matrix_index,mass_matrix_index] = self.M[mass_matrix_index,mass_matrix_index] + self.W[element_index]/4
    # def initialize_reference_shape_matrix(self,element_index,element_node):
    #     print(f'initializing discrete gradient (Dm and DmINV) for a FEM mesh')
    #     self.Dm[3 * element_index : 3 * (element_index + 1), : ] = element_node.transpose().dot(self.G)
    #     self.DmINV[3 * element_index : 3 * (element_index + 1), : ] = np.linalg.inv(element_node.transpose().dot(self.G))
    # def initialize_deformation_gradient_transform(self,element_index,element_node):
    #     print(f'initializing deformation gradient transform (T) for a FEM mesh')
    #     self.T[9*element_index:9*(element_index+1),:] = np.kron((self.G.dot(self.DmINV[3 * element_index : 3 * (element_index + 1), : ])).transpose(), self.Iv )
    # def initialize_stiffness_matrix_indices(self,element_index,element_node):
    #     print(f'initializing stiffness matrix (ii,jj) for a FEM mesh')
    #     self.ii = np.array([])
    #     self.jj = np.array([])
    # def calculate_deformation_gradient(self,element_index,element_node):
    #     print(f'calculating deformation gradient F for a FEM mesh')
    #     self.deformation_gradient = np.array([])
    #     self.inv_deformation_gradient = np.array([])
    # def elemental_calculation(self, calculation_list = []):
    #     for element_index in range(self.elements.shape[0]):
    #         element_node = self.vertices[self.elements[element_index,:]]
    #         for calculation in calculation_list:
    #             calculation(element_index,element_node)
