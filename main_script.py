from pyvista.utilities.parametric_objects import surface_from_para
from EnvironmentLoader import EnvironmentLoader
import numpy as np
import Mesh

if __name__ == "__main__":
    draw_frame = True
    env = EnvironmentLoader()
    env_mediator = env.load("example-env.json")

    num_frames = 200
    filepath = "results/view"
    surface_triangulation = []
    for i in range(num_frames):
        env_mediator.request_frame()
        if draw_frame:
            print(f'drawing environment')
            verts = env_mediator.simulatable_objects[0].mesh.vertices
            elems = env_mediator.simulatable_objects[0].mesh.elements
            if not surface_triangulation:
                surface_triangulation = Mesh.Mesh.surface_triangulation(verts,elems).tolist()
            with open(filepath+str(i)+".obj", 'w') as f:
                f.write("# OBJ file\n")
                for v in verts:
                    f.write('v {:2.4} {:2.4} {:2.4}\n'.format(v[0],v[1],v[2]))
                for p in surface_triangulation:
                    f.write("f")
                    for i in p:
                        f.write(f" {i+1}" )
                    f.write("\n")
