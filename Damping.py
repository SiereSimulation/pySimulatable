from enum import Enum

class DampingModel(Enum):
    Rayleigh = 1
    Proportional = 2
class Damping:
    def __init__(self, model:DampingModel = DampingModel.Rayleigh) -> None:
        print(f'{type(self).__name__} created')
        if model == DampingModel.Rayleigh:
            self.a = 0
            self.b = 0