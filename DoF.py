import numpy as np

class DoF:
    def __init__(self, positions : np.array = np.array([0]), velocities : np.array = np.array([0]), free_indices : np.array = np.array([0])) -> None:
        print(f'{type(self).__name__} created')
        self.positions = positions
        self.velocities = velocities
        self.free_indices = free_indices
    def get_positions(self):
        return self.positions[self.free_indices]
    def get_velocities(self):
        return self.velocities[self.free_indices]
    def get_full_positions(self):
        return self.positions
    def get_full_velocities(self):
        return self.velocities
    def set_positions(self, positions):
        pass
    def set_velocities(self, velocities):
        pass
