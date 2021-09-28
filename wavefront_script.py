import pyredner
import torch

objects = pyredner.load_obj("shirt_lp__corona.obj", return_objects=True)
camera = pyredner.automatic_camera_placement(objects, resolution=(512, 512))
scene = pyredner.Scene(camera = camera, objects = objects)
light = pyredner.DirectionalLight(direction = torch.tensor((1.0, -1.0, 1.0), device = pyredner.get_device()),intensity = torch.tensor((2.0, 3.0, 2.0), device = pyredner.get_device()))

img = pyredner.render_deferred(scene = scene, lights = [light])
# img = pyredner.render_albedo(scene)
img_file = 't_shirt.png'
pyredner.imwrite(img, img_file)