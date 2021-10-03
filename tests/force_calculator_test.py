import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ForceCalculator
import Simulatable
import Mesh
import Material
import pytest
import numpy as np
from pathlib import Path
import scipy
from scipy.io import loadmat
from numpy.linalg import norm
from scipy.sparse import linalg as slinalg
from numpy.random import default_rng
import random

def tolerance():
    return 1e-8

def stiffness():
    return 1e5


def assets_directory():
    return str(Path(__file__).resolve().parent.parent.parent) + "/assets/"

def load_bar():
    mesh = Mesh.Mesh()
    verts, elem = Mesh.Mesh.read_tetgen_file(assets_directory() + "bar/bar.node",assets_directory() + "bar/bar.ele")
    mesh.load_mesh(verts,elem)
    material = Material.FEMMaterial(density=1000,youngs=stiffness(),poisson=0.45,mtype=Material.ElasticityModel.neohookean)
    bar = Simulatable.SolidObject(dimension=3,material=material,mesh=mesh)
    
    return bar

def load_arma():
    mesh = Mesh.Mesh()
    verts, elem = Mesh.Mesh.read_tetgen_file(assets_directory() + "armadillo/arma_6.node",assets_directory() + "armadillo/arma_6.ele")
    mesh.load_mesh(verts,elem)
    # the following parameter is hard-coded to match matlab data
    material = Material.FEMMaterial(density=1000,youngs=1e5,poisson=0.45,mtype=Material.ElasticityModel.neohookean)
    arma = Simulatable.SolidObject(dimension=3,material=material,mesh=mesh)
    return arma

def test_FEM_discretization_calculator_constructor():
    fake_material = Material.Material()
    fake_mesh = Mesh.Mesh()
    fake_object = Simulatable.SolidObject(3, fake_material, fake_mesh)
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(fake_object)
    assert force_calculator.solid_object == fake_object

# change this to fixtures, once I understand what fixture is
bar = load_bar()
arma = load_arma()
arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")

def test_FEM_force_calculator_initialization():
    
    ForceCalculator.FEMDiscretizationCalculator(bar)
    bar_test_data = loadmat(assets_directory()+"bar/bar_test.mat")
    assert norm(bar_test_data["Dm"] - bar.discretization.Dm) < tolerance()
    assert norm(bar_test_data["DmINV"] - bar.discretization.DmINV) < tolerance()
    assert norm(bar_test_data["T"] - bar.discretization.T) < tolerance()

    ForceCalculator.FEMDiscretizationCalculator(arma)
    assert norm(arma_test_data["Dm"] - arma.discretization.Dm) < tolerance()
    assert norm(arma_test_data["DmINV"] - arma.discretization.DmINV) < tolerance()
    assert norm(arma_test_data["T"] - arma.discretization.T) < tolerance()
    assert slinalg.norm(arma_test_data["M"] - arma.discretization.M) < tolerance()
    assert norm(arma_test_data["W"] - arma.discretization.W) < tolerance()

    
def test_FEM_force_calculator_calculate_neohookean():
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    
    arma.dof.positions = (arma_test_data["node_50"] - arma.mesh.undeformed_vertices).flatten()
    arma.update_mesh()
    force_calculator.calculate()
    assert norm(arma_test_data["Ds_50"] - arma.discretization.Ds) < tolerance()
    assert norm(arma_test_data["F_50"] - arma.discretization.F) < tolerance()
    assert norm(arma_test_data["FINV_50"] - arma.discretization.FINV) < tolerance()
    assert norm(arma_test_data["internal_force_50"].flatten() - arma.internal_force.force) < tolerance()
    assert slinalg.norm(arma_test_data["K_50"] + arma.internal_force.force_gradient, ord=1) < tolerance()

def test_FEM_force_calculator_calculate_neohookean_directional_derivative():
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(bar)
    n = bar.dof.positions.size
    ep = 1e-9
    bar.dof.set_positions(np.zeros((n,1)).flatten())
    force_calculator.calculate()
    force = bar.internal_force.force
    K = -bar.internal_force.force_gradient

    x = np.random.rand(n,1).flatten()
    deform_direction = x / norm(x)
    deformation = ep*deform_direction
    bar.dof.set_positions(deformation)
    bar.update_mesh()
    force_calculator.calculate()
    force_new = bar.internal_force.force
    assert norm ((force_new - force)/ep + (K @ deform_direction)) < tolerance() * 1e5
    

if __name__ == "__main__":
    test_FEM_force_calculator_initialization()
    test_FEM_force_calculator_calculate_neohookean()
    test_FEM_discretization_calculator_constructor()
    test_FEM_force_calculator_calculate_neohookean_directional_derivative()