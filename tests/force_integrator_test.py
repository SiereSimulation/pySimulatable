import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ForceCalculator
import Simulatable
import Mesh
import Material
import pytest
import numpy as np
from pathlib import Path
from scipy.io import loadmat

def assets_directory():
    return str(Path(__file__).resolve().parent.parent) + "/assets/"