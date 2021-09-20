import pywavefront
from pywavefront import visualization

scene = pywavefront.Wavefront("woman_outfit.obj")
# scene.parse()

visualization.draw(scene)