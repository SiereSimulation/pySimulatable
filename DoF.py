class DoF:
    def __init__(self, positions = 0, velocities = 0, free_indices = 0) -> None:
        print(f'{type(self).__name__} created')
        self.positions = positions
        self.velocities = velocities
        self.free_indices = free_indices
    def get_positions(self):
        return self.positions(self.free_indices)
    def get_velocities(self):
        return self.velocities(self.free_indices)
