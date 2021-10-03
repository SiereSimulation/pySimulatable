import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ForceResult
import numpy as np
from numpy.linalg import norm
from scipy.sparse import random as srandom
from scipy.sparse import linalg as slinalg
from scipy import stats
from numpy.random import default_rng
import random

def tolerance():
    return 1e-8

def test_force_result_constructor():
    force = ForceResult.ForceResult()

    assert force.force.size == 0
    assert force.energy == 0
    assert force.force_gradient.size == 0

def test_getter_setter():
    force = ForceResult.ForceResult()
    rand_force = np.random.rand(5,1)
    force.set_force(rand_force)
    assert norm(force.get_force() - rand_force) < tolerance()

    rand_energy = random.random()
    force.set_energy(rand_energy)
    assert norm(force.get_energy() - rand_energy) < tolerance()

    rng = default_rng()
    rvs = stats.poisson(25, loc=10).rvs
    S = srandom(3, 4, density=0.25, random_state=rng, data_rvs=rvs, format='csc')
    force.set_force_gradient(S)
    assert slinalg.norm(S - force.get_force_gradient()) < tolerance()

def test_add_force():
    force = ForceResult.ForceResult()
    rand_force_1 = np.random.rand(5,1)
    rand_force_2 = np.random.rand(5,1)
    force.force = rand_force_1
    force.add_force(rand_force_2)
    assert norm(force.get_force() - rand_force_1 - rand_force_2 ) < tolerance()

def test_add_force_gradient():
    force = ForceResult.ForceResult()
    rng = default_rng()
    rvs_1 = stats.poisson(25, loc=10).rvs
    S_1 = srandom(3, 4, density=0.25, random_state=rng, data_rvs=rvs_1, format='csc')
    rvs_2 = stats.poisson(55, loc=10).rvs
    S_2 = srandom(3, 4, density=0.5, random_state=rng, data_rvs=rvs_2, format='csc')
    force.set_force_gradient(S_1)
    force.add_force_gradient(S_2)
    assert slinalg.norm(S_1 + S_2 - force.get_force_gradient()) < tolerance()

def test_plus_operator():
    force_1 = ForceResult.ForceResult()
    force_2 = ForceResult.ForceResult()
    rand_force_1 = np.random.rand(5,1)
    rand_force_2 = np.random.rand(5,1)
    force_1.force = rand_force_1
    force_2.force = rand_force_2

    rng = default_rng()
    rvs_1 = stats.poisson(25, loc=10).rvs
    S_1 = srandom(3, 4, density=0.25, random_state=rng, data_rvs=rvs_1, format='csc')
    rvs_2 = stats.poisson(55, loc=10).rvs
    S_2 = srandom(3, 4, density=0.5, random_state=rng, data_rvs=rvs_2, format='csc')
    force_1.set_force_gradient(S_1)
    force_2.set_force_gradient(S_2)
    
    force_3 = force_1 + force_2
    assert slinalg.norm(S_1 + S_2 - force_3.get_force_gradient()) < tolerance()
    assert norm(rand_force_1 + rand_force_2 - force_3.get_force()) < tolerance()


if __name__ == "__main__":
    test_force_result_constructor()
    test_getter_setter()
    test_add_force()
    test_add_force_gradient()
    test_plus_operator()