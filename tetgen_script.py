import pyvista as pv
import tetgen
import numpy as np
from scipy.io import savemat
pv.set_plot_theme('document')
sphere = pv.Sphere()
tet = tetgen.TetGen(sphere)
tet.tetrahedralize(order=1, mindihedral=20, minratio=1.5)

mdic = {"node": tet.node, "elem": tet.elem}

savemat("sphere.mat",mdic)
# grid = tet.grid
# pv.start_xvfb()