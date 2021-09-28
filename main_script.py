from pyvista.utilities.parametric_objects import surface_from_para
from EnvironmentLoader import EnvironmentLoader
import numpy as np
import Mesh
from common.renderer import render_frames

if __name__ == "__main__":
    draw_frame = True
    env = EnvironmentLoader()
    env_mediator = env.load("./python/example-env.json")

    num_frames = 200
    filepath = "./python/tests/results/view"
    surface_triangulation = []
    all_verts = []
    for i in range(num_frames):
        env_mediator.request_frame()
        if draw_frame:
            print(f'drawing environment')
            verts = env_mediator.simulatable_objects[0].mesh.vertices
            elems = env_mediator.simulatable_objects[0].mesh.elements
            if not surface_triangulation:
                surface_triangulation = Mesh.Mesh.surface_triangulation(verts,elems).tolist()

            with open('{filepath}{index:04d}.obj'.format(filepath=filepath,index=i), 'w') as f:
                f.write("# OBJ file\n")
                for v in verts:
                    f.write('v {:2.4} {:2.4} {:2.4}\n'.format(v[0],v[1],v[2]))
                for p in surface_triangulation:
                    f.write("f")
                    for i in p:
                        f.write(f" {i+1}" )
                    f.write("\n")
            all_verts.append(verts)
    ## temporal render calls -> do nothing for now 
    render_frames(all_verts, surface_triangulation, basepath="./python/tests/results/render")
    

    
