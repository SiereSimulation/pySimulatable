import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import DoF
import Mesh
import numpy as np
from numpy.linalg import norm
from scipy.sparse import random as srandom
from scipy.sparse import linalg as slinalg
from scipy import stats
from numpy.random import default_rng
import random
from pathlib import Path


def assets_directory():
    return str(Path(__file__).resolve().parent.parent.parent) + "/assets/"


def test_dof_constructor():
    dof = DoF.DoF()
    assert dof.positions.size == 0
    assert dof.velocities.size == 0
    assert dof.free_indices.size == 0

def test_dof_initialize_from_mesh():
    dof = DoF.DoF()
    mesh = Mesh.Mesh()
    dof.initialize_from_mesh(mesh)
    assert dof.positions.size == mesh.undeformed_vertices.size
    assert dof.velocities.size == mesh.undeformed_vertices.size
    assert dof.free_indices.size == mesh.undeformed_vertices.size

    verts, elem = Mesh.Mesh.read_tetgen_file(assets_directory()+"bar/bar.node", assets_directory() +"bar/bar.ele")
    mesh.load_mesh(verts,elem)
    dof.initialize_from_mesh(mesh)
    assert dof.positions.size == mesh.undeformed_vertices.size
    assert dof.velocities.size == mesh.undeformed_vertices.size
    assert dof.free_indices.size == mesh.undeformed_vertices.size
    assert np.max(dof.free_indices - np.arange(dof.positions.size)) == 0

def test_getter_setter():
    dof = DoF.DoF()
    n = 5
    positions = np.random.rand(n,1).flatten()
    velocities = np.random.rand(n,1).flatten()
    free_indices = np.arange(n)
    dof.set_full_positions(positions)
    dof.set_full_velocities(velocities)
    dof.set_free_indices(free_indices)
    assert np.max(dof.get_positions() - positions) == 0
    assert np.max(dof.get_velocities() - velocities) == 0
    assert np.max(dof.get_free_indices() - free_indices) == 0

def test_getter_setter_with_constraints():
    dof = DoF.DoF()
    mesh = Mesh.Mesh()
    verts, elem = Mesh.Mesh.read_tetgen_file(assets_directory()+"bar/bar.node", assets_directory() +"bar/bar.ele")
    mesh.load_mesh(verts,elem)
    dof.initialize_from_mesh(mesh)
    n = dof.get_free_indices().size
    n_constraints = 5
    assert n - n_constraints > 0
    for i in range(n_constraints):
        free_indices = dof.get_free_indices()
        index_to_remove = np.random.randint(0,free_indices.size)
        mask = np.ones(free_indices.size,dtype=bool)
        mask[[index_to_remove]] = False
        free_indices = free_indices[mask,...]
        dof.set_free_indices(free_indices)
    assert dof.get_free_indices().size == n - n_constraints
    assert dof.get_positions().size == n - n_constraints
    assert dof.get_velocities().size == n - n_constraints

    positions = np.random.rand(n-n_constraints,1).flatten()
    velocities = np.random.rand(n-n_constraints,1).flatten()
    dof.set_positions(positions)
    dof.set_velocities(velocities)
    assert np.max(dof.get_positions() - positions) == 0
    assert np.max(dof.get_velocities() - velocities) == 0
    

if __name__ == "__main__":
    test_getter_setter()
    test_getter_setter_with_constraints()