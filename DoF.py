import numpy as np
import Mesh
class DoF:
    def __init__(self, positions : np.array = np.array([]), velocities : np.array = np.array([]), free_indices : np.array = np.array([], np.int32)) -> None:
        print(f'{type(self).__name__} created')
        self.positions = positions
        self.velocities = velocities
        self.free_indices = free_indices
    def initialize_from_mesh(self,mesh: Mesh.Mesh):
        self.positions = np.zeros(mesh.undeformed_vertices.size)
        self.velocities = np.zeros(mesh.undeformed_vertices.size)
        self.free_indices = np.arange(mesh.undeformed_vertices.size)
    def get_positions(self):
        return self.positions[self.free_indices]
    def get_velocities(self):
        return self.velocities[self.free_indices]
    def get_free_indices(self):
        return self.free_indices
    def get_full_positions(self):
        return self.positions
    def get_full_velocities(self):
        return self.velocities
    def set_full_positions(self, positions):
        self.positions = positions
    def set_full_velocities(self, velocities):
        self.velocities = velocities
    def set_positions(self, positions):
        self.positions[self.free_indices] = positions
    def set_velocities(self, velocities):
        self.velocities[self.free_indices] = velocities
    def set_free_indices(self, free_indices):
        self.free_indices = free_indices

