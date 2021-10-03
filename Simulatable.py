from ForceResult import ForceResult
from DoF import DoF
from Discretization import Discretization
import numpy as np
import Material
import Mesh
from scipy.sparse import csc, csc_matrix
from RenderData import RenderData
class Constraint:
    def __init__(self,axis,location,tolerance) -> None:
        self.axis = axis
        self.location = location
        self.tolerance = tolerance

class ISimulatable:
    def __init__(self):
        print(f'{type(self).__name__} created')
    def update(self,simulator):
        simulator.simulate()


class SolidObject(ISimulatable):
    def __init__(self,dimension,material:Material.Material ,mesh: Mesh.Mesh):
        super().__init__()
        print(f'{type(self).__name__} created')
        self.dimension = dimension
        self.material = material
        self.mesh = mesh
        self.dof = DoF()
        self.dof.initialize_from_mesh(mesh)
        self.internal_force = ForceResult()
        self.external_force = ForceResult()
        self.damping_force = ForceResult()
        self.discretization = Discretization()
        self.constraint_list = []
    def add_constraint(self, constraint):
        self.constraint_list.append(constraint)
    def get_num_vertices(self) -> int:
        return int(self.mesh.vertices.size/self.dimension)
    def get_num_elements(self) -> int:
        return self.mesh.elements.shape[0]
    def get_mesh(self) -> Mesh.Mesh:
        return self.mesh
    def get_material(self) -> Material.Material:
        return self.material
    def get_dof(self) -> DoF:
        return self.dof
    def get_mass(self) -> csc_matrix:
        return self.discretization.M
    def get_internal_force(self):
        return self.internal_force
    def get_external_force(self):
        return self.external_force
    def get_damping_force(self):
        return self.damping_force
    def add_internal_force(self,force):
        self.internal_force = self.internal_force + force
    def add_external_force(self,force):
        self.external_force = self.external_force + force
    def add_damping_force(self,force):
        self.damping_force = self.damping_force + force
    
    def update(self, simulator):
        # can do something to the object before simulation, like set constraints
        self.apply_constraints()
        simulator.simulate(self)
        # can do something after, like updating the mesh
        self.update_mesh()
    def set_axis_constraints(self, axis, location, tolerance):
        max_in_columns = np.amax(self.mesh.undeformed_vertices, axis=0)
        min_in_columns = np.amin(self.mesh.undeformed_vertices, axis=0)
        if axis == 'x':
            axis_val = 0
        elif axis == 'y':
            axis_val = 1
        elif axis == 'z':
            axis_val = 2
        max_val = max_in_columns[axis_val]
        min_val = min_in_columns[axis_val]
        constraint_range = (max_val - min_val) * tolerance/100
        if location == "top":
            current_free_indices = np.nonzero(np.tile((self.mesh.undeformed_vertices[:,axis_val] < max_val - constraint_range),(3,1)).flatten("F"))[0]
        else:
            current_free_indices = np.nonzero(np.tile((self.mesh.undeformed_vertices[:,axis_val] > min_val + constraint_range),(3,1)).flatten("F"))[0]
        old_free_indices = self.dof.free_indices
        # new indices are in the both sets, i.e. the intersection
        new_free_indices = np.intersect1d(old_free_indices,current_free_indices)
        self.dof.set_free_indices(new_free_indices)
    def apply_constraints(self):
        for constraint in self.constraint_list:
            self.set_axis_constraints(axis=constraint.axis, location=constraint.location, tolerance=constraint.tolerance)
    def update_mesh(self):
        self.mesh.deform(np.reshape(self.dof.get_full_positions(),(-1,3)))

class Environment(ISimulatable):

    def __init__(self):
        print(f'{type(self).__name__} created')
        self.simulatable_objects = []
        self.gravity = np.array([0,0,-9.8])     
        self.environment_simulator = None
        self.render_data = None
        
    def add(self, simulatable):
        print(f'adding simulatable')
        self.simulatable_objects.append(simulatable)
     
    def set_gravity(self, gravity):
        self.gravity = gravity
    def calculate_gravity(self):
        print(f'calculating gravity')
        for simulatable in self.simulatable_objects:
            simulatable.external_force.force = simulatable.get_mass() @ np.tile(self.gravity,(simulatable.get_num_vertices(),1)).flatten()
    def collision_detection(self):
        print(f'collision detection')
    def contact_resolution(self):
        print(f'contact resolution')

    def request_frame(self):
        self.update(self.environment_simulator)
    def update(self, simulator):
        # can do something with the environment before simulation
        simulator.simulate(self)
        # can do something with the environment after simulation