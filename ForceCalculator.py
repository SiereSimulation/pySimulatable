from Discretization import FEMDiscretization
from numpy.core.fromnumeric import transpose
from Material import Material, ElasticityModel
from ForceResult import ForceResult
from abc import ABC, abstractmethod
from Simulatable import SolidObject
import numpy as np
from scipy.sparse import csc_matrix
from scipy.linalg import logm
import math

class IForceCalculator(ABC):
    def __init__(self,simulatable) -> None:
        print(f'{type(self).__name__} created')
        self.simulatable = simulatable
    def calculate(self) -> None:
        pass

class FEMDiscretizationCalculator(IForceCalculator):
    Iv = np.eye(3) # Identity for vector
    Im = np.eye(9) # Identity for matrix
    Kmm =   np.array( \
            [[1,     0,     0,     0,     0,     0,     0,     0,     0], \
            [0,     0,     0,     1,     0,     0,     0,     0,     0], \
            [0,     0,     0,     0,     0,     0,     1,     0,     0], \
            [0,     1,     0,     0,     0,     0,     0,     0,     0], \
            [0,     0,     0,     0,     1,     0,     0,     0,     0], \
            [0,     0,     0,     0,     0,     0,     0,     1,     0], \
            [0,     0,     1,     0,     0,     0,     0,     0,     0], \
            [0,     0,     0,     0,     0,     1,     0,     0,     0], \
            [0,     0,     0,     0,     0,     0,     0,     0,     1]]\
    )
    G = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]])
    dimension = 3
    def __init__(self,solid_object: SolidObject) -> None:
        print(f'{type(self).__name__} created')
        self.solid_object = solid_object
        self.solid_object.discretization = FEMDiscretization(solid_object.dimension,solid_object.mesh)
        self.stiffness_matrix_index_count = 0
        self.initialize_FEM_discretization()
        
    def initialize_FEM_discretization(self):
        print(f'initializing FEM mesh')
        self.discretization = FEMDiscretization(self.solid_object.dimension,self.solid_object.mesh)
        for element_index in range(self.solid_object.mesh.elements.shape[0]):
            element_node = self.solid_object.mesh.undeformed_vertices[self.solid_object.mesh.elements[element_index,:]]
            self.initialize_reference_shape_matrix_and_transform(element_index,element_node)
            self.initialize_volume_and_mass(element_index,element_node)
            self.initialize_stiffness_matrix_indices(element_index)
        self.solid_object.discretization = self.discretization


    def initialize_volume_and_mass(self,element_index,element_node):
        self.discretization.W[element_index] = np.abs(np.linalg.det(element_node.transpose().dot(self.G)))/6
        for element in self.solid_object.mesh.elements[element_index,:]:
            for mass_matrix_index in range(element*3, (element+1)*3):
                self.discretization.M[mass_matrix_index,mass_matrix_index] = self.discretization.M[mass_matrix_index,mass_matrix_index] + self.solid_object.material.density*self.discretization.W[element_index]/4
                
    def initialize_reference_shape_matrix_and_transform(self,element_index,element_node):
        # print(f'initializing discrete gradient (Dm and DmINV) and transform (T) for a FEM mesh')
        self.discretization.Dm[3 * element_index : 3 * (element_index + 1), : ] = element_node.transpose().dot(self.G)
        self.discretization.DmINV[3 * element_index : 3 * (element_index + 1), : ] = np.linalg.inv(element_node.transpose().dot(self.G))
        self.discretization.T[9*element_index:9*(element_index+1),:] = np.kron((self.G.dot(self.discretization.DmINV[3 * element_index : 3 * (element_index + 1), : ])).transpose(), self.Iv )

    def initialize_stiffness_matrix_indices(self,element_index):
        # print(f'initializing stiffness matrix (ii,jj) for a FEM mesh')
        for ti in range(4):
            for tj in range(4):
                self.discretization.ii[self.stiffness_matrix_index_count:self.stiffness_matrix_index_count+9] = \
                    np.tile(np.arange(3*self.solid_object.mesh.elements[element_index,ti],3*(self.solid_object.mesh.elements[element_index,ti]+1)),(1,3))
                self.discretization.jj[self.stiffness_matrix_index_count:self.stiffness_matrix_index_count+9] = \
                    np.tile(np.arange(3*self.solid_object.mesh.elements[element_index,tj],3*(self.solid_object.mesh.elements[element_index,tj]+1)),(3,1)).flatten("F")
                self.stiffness_matrix_index_count = self.stiffness_matrix_index_count + 9
        
    def calculate(self):
        print(f'calculating discretized quantities (forces, force grad, etc)')
        force = np.zeros(self.solid_object.dof.get_full_positions().shape[0])
        energy = 0
        
        sA = np.empty_like(self.solid_object.discretization.ii)
        stiffness_matrix_index = 0
        for element_index in range(self.solid_object.mesh.elements.shape[0]):
            element_node = self.solid_object.mesh.vertices[self.solid_object.mesh.elements[element_index,:]]
            self.solid_object.discretization.Ds[3 * element_index : 3 * (element_index + 1), : ] = element_node.transpose().dot(self.G)
            tF = element_node.transpose().dot(self.G) @ self.solid_object.discretization.DmINV[3 * element_index : 3 * (element_index + 1), : ]
            # dont need to calculate FINV unless it's neohookean, but we calculate it anyway for now
            tFINV = np.linalg.inv(tF)
            self.solid_object.discretization.F[3 * element_index : 3 * (element_index + 1), : ] = tF
            self.solid_object.discretization.FINV[3 * element_index : 3 * (element_index + 1), : ] = tFINV
            tT = self.solid_object.discretization.T[9*element_index:9*(element_index+1),:]
            J = np.linalg.det(tF)
            Kk = self.Kmm @ np.kron(tFINV.transpose(), tFINV)
            if self.solid_object.material.mtype == ElasticityModel.neohookean:
                
                # for stiffness matrix
                C = self.solid_object.material.mu * self.Im + self.solid_object.material.mu * Kk \
                    - self.solid_object.material.lambd * (math.log(J)*Kk) \
                    + self.solid_object.material.lambd * (self.Kmm@(tFINV.flatten("F").reshape(-1,1)@np.reshape(tFINV,(1,9))))    
                
                # for force
                P = self.solid_object.material.mu * (tF - tFINV.transpose()) + self.solid_object.material.lambd * math.log(J) * tFINV.transpose()
            elif self.solid_object.material.mtype == ElasticityModel.stable_neohookean:
                pass
            elif self.solid_object.material.mtype == ElasticityModel.stvk:
                print(f'stvk not implemented yet')
                
            H = -self.solid_object.discretization.W[element_index] * P @ (self.solid_object.discretization.DmINV[3 * element_index : 3 * (element_index + 1), : ].transpose())
            Kt = self.solid_object.discretization.W[element_index] * tT.transpose() @ C @ tT
            Kt = 1/2 * (Kt + Kt.transpose())
            i = self.solid_object.mesh.elements[element_index,0]
            j = self.solid_object.mesh.elements[element_index,1]
            k = self.solid_object.mesh.elements[element_index,2]
            l = self.solid_object.mesh.elements[element_index,3]
            force[3*i:3*(i+1)] = force[3*i:3*(i+1)] + H[:,0]
            force[3*j:3*(j+1)] = force[3*j:3*(j+1)] + H[:,1]
            force[3*k:3*(k+1)] = force[3*k:3*(k+1)] + H[:,2]
            force[3*l:3*(l+1)] = force[3*l:3*(l+1)] - H[:,0] - H[:,1] - H[:,2]
            for ti in range(4):
                for tj in range(4):
                    sA[stiffness_matrix_index: stiffness_matrix_index+9] = Kt[3*ti:3*(ti+1),3*tj:3*(tj+1)].flatten("F")
                    stiffness_matrix_index = stiffness_matrix_index + 9
            # sA[stiffness_matrix_index:stiffness_matrix_index+144] = Kt.flatten("F")
            # stiffness_matrix_index = stiffness_matrix_index + 144
        force_gradient = csc_matrix((-sA, (self.solid_object.discretization.ii, self.solid_object.discretization.jj)), shape=(self.solid_object.dof.get_full_positions().shape[0], self.solid_object.dof.get_full_positions().shape[0]))
        self.solid_object.internal_force.set_energy(energy)
        self.solid_object.internal_force.set_force(force)
        self.solid_object.internal_force.set_force_gradient(force_gradient)

        self.solid_object.damping_force.set_force(self.solid_object.material.damping_model.a * self.solid_object.get_mass() @ self.solid_object.dof.get_full_velocities() - self.solid_object.material.damping_model.b*force_gradient @ self.solid_object.dof.get_full_velocities())

        self.solid_object.damping_force.set_force_gradient(self.solid_object.material.damping_model.a * self.solid_object.get_mass() - self.solid_object.material.damping_model.b*force_gradient)

        

        

    
        


