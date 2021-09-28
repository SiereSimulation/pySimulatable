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

def tolerance():
    return 1e-8

def assets_directory():
    return str(Path(__file__).resolve().parent.parent) + "/assets/"

def load_bar():
    mesh = Mesh.Mesh()
    verts, elem = Mesh.Mesh.read_tetgen_file(assets_directory() + "bar/bar.node",assets_directory() + "bar/bar.ele")
    mesh.load_mesh(verts,elem)
    material = Material.FEMMaterial(density=1000,youngs=1e5,poisson=0.45,mtype=Material.ElasticityModel.neohookean)
    bar = Simulatable.SolidObject(dimension=3,material=material,mesh=mesh)
    
    return bar

def load_arma():
    mesh = Mesh.Mesh()
    verts, elem = Mesh.Mesh.read_tetgen_file(assets_directory() + "armadillo/arma_6.node",assets_directory() + "armadillo/arma_6.ele")
    mesh.load_mesh(verts,elem)
    material = Material.FEMMaterial(density=1000,youngs=1e5,poisson=0.45,mtype=Material.ElasticityModel.neohookean)
    arma = Simulatable.SolidObject(dimension=3,material=material,mesh=mesh)
    return arma

def test_FEM_force_calculator_initialize_reference_shape_matrices():
    
    bar = load_bar()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(bar)
    bar_test_data = loadmat(assets_directory()+"bar/bar_test.mat")
    assert np.max(bar_test_data["Dm"] - bar.discretization.Dm) < tolerance()
    assert np.max(bar_test_data["DmINV"] - bar.discretization.DmINV) < tolerance()
    assert np.max(bar_test_data["T"] - bar.discretization.T) < tolerance()

    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")
    assert np.max(arma_test_data["Dm"] - arma.discretization.Dm) < tolerance()
    assert np.max(arma_test_data["DmINV"] - arma.discretization.DmINV) < tolerance()
    assert np.max(arma_test_data["T"] - arma.discretization.T) < tolerance()

def test_FEM_force_calculator_deform_shape_matrices():
    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")

    arma.mesh.deform(arma_test_data["node_50"] - arma.mesh.undeformed_vertices)
    force_calculator.calculate_deformation_gradient()
    assert np.max(arma_test_data["Ds_50"] - arma.discretization.Ds) < tolerance()
    

    arma.mesh.deform(arma_test_data["node_100"] - arma.mesh.undeformed_vertices)
    force_calculator.calculate_deformation_gradient()
    assert np.max(arma_test_data["Ds_100"] - arma.discretization.Ds) < tolerance()

def test_FEM_force_calculator_initialize_volume_and_mass():
    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")
    assert np.max(arma_test_data["M"] - arma.discretization.M) < tolerance()
    assert np.max(arma_test_data["W"] - arma.discretization.W) < tolerance()
    
def test_FEM_force_calculator_initialize_deformation_gradient():
    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    force_calculator.calculate_deformation_gradient()
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")
        
    assert np.max(arma_test_data["F"] - arma.discretization.F) < tolerance()
    assert np.max(arma_test_data["FINV"] - arma.discretization.FINV) < tolerance()


def test_FEM_force_calculator_deformation_gradient():
    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")

    arma.mesh.deform(arma_test_data["node_50"] - arma.mesh.undeformed_vertices)
    force_calculator.calculate_deformation_gradient()
    assert np.max(arma_test_data["F_50"] - arma.discretization.F) < tolerance()
    assert np.max(arma_test_data["FINV_50"] - arma.discretization.FINV) < tolerance()

    arma.mesh.deform(arma_test_data["node_100"] - arma.mesh.undeformed_vertices)
    force_calculator.calculate_deformation_gradient()
    assert np.max(arma_test_data["F_100"] - arma.discretization.F) < tolerance()
    assert np.max(arma_test_data["FINV_100"] - arma.discretization.FINV) < tolerance()

def test_FEM_force_calculator_internal_force_neohookean():
    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")

    arma.dof.positions = (arma_test_data["node_50"] - arma.mesh.undeformed_vertices).flatten()
    # arma.mesh.deform(arma_test_data["node_50"] - arma.mesh.undeformed_vertices)
    # force_calculator.calculate_deformation_gradient()
    force_calculator.calculate()
    assert np.max(arma_test_data["internal_force_50"].flatten() - arma.internal_force.force) < tolerance()
    
    # arma.mesh.deform(arma_test_data["node_100"] - arma.mesh.undeformed_vertices)
    arma.dof.positions = (arma_test_data["node_100"] - arma.mesh.undeformed_vertices).flatten()
    force_calculator.calculate_deformation_gradient()
    force_calculator.calculate()
    assert np.max(arma_test_data["internal_force_100"].flatten() - arma.internal_force.force) < tolerance()
    

def test_FEM_force_calculator_internal_force_gradient_neohookean():
    arma = load_arma()
    force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
    arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")

    arma.dof.positions = (arma_test_data["node_50"] - arma.mesh.undeformed_vertices).flatten()
    force_calculator.calculate()
    assert np.max(arma_test_data["K_50"] + arma.internal_force.force_gradient) < tolerance()
    
    arma.dof.positions = (arma_test_data["node_100"] - arma.mesh.undeformed_vertices).flatten()
    force_calculator.calculate()
    assert np.max(arma_test_data["K_100"] + arma.internal_force.force_gradient) < tolerance()
    


# def test_FEM_force_calculator_initialize_internal_force_gradient_neohookean():
#     arma = load_arma()
#     force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
#     force_calculator.calculate_deformation_gradient()
#     arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")
        
#     assert np.max(arma_test_data["F"] - arma.discretization.F) < 1e-10
#     assert np.max(arma_test_data["FINV"] - arma.discretization.FINV) < 1e-10

# def test_FEM_force_calculator_initialize_internal_energy_neohookean():
#     arma = load_arma()
#     force_calculator = ForceCalculator.FEMDiscretizationCalculator(arma)
#     force_calculator.calculate_deformation_gradient()
#     arma_test_data = loadmat(assets_directory()+"armadillo/arma_6_test.mat")
        
#     assert np.max(arma_test_data["F"] - arma.discretization.F) < 1e-10
#     assert np.max(arma_test_data["FINV"] - arma.discretization.FINV) < 1e-10



if __name__ == "__main__":
    test_FEM_force_calculator_internal_force_gradient_neohookean()
    test_FEM_force_calculator_internal_force_neohookean()
    test_FEM_force_calculator_initialize_reference_shape_matrices()
    test_FEM_force_calculator_initialize_volume_and_mass()
    test_FEM_force_calculator_initialize_deformation_gradient()
    test_FEM_force_calculator_deform_shape_matrices()
    test_FEM_force_calculator_deformation_gradient()