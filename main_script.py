from pyvista.utilities.parametric_objects import surface_from_para
from EnvironmentLoader import EnvironmentLoader
import numpy as np
import Mesh
from common.renderer import PbrtRender, BlenderRender

if __name__ == "__main__":
    draw_frame = True
    env = EnvironmentLoader()
    env_mediator = env.load("./python/bar-env.json")

    num_frames = 2
    filepath = "./python/tests/results/view"
    surface_triangulation = []
    all_export_files = []
    for i in range(num_frames):
        env_mediator.request_frame()
        all_export_files.append('view{index:04d}.obj'.format(index=i))
        if draw_frame:
            print(f'drawing environment frame {i}')
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
    renderer = BlenderRender(env_mediator.render_data)
    renderer.render_animation(all_export_files)

    
