import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

class Cactus(Object3D) :
    def __init__(self,id) :
        self.id = id
        self.mesh = Mesh.load_obj('cactus.obj')
        self.mesh.normalize()
        self.mesh.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
        self.tr = Transformation3D()
        self.vao = self.mesh.load_to_gpu()

        self.tr.translation.y = -np.amin(self.mesh.vertices, axis=0)[1]
        self.tr.rotation_center.z = 0.5


    def Texture(self, texture) :
        self.texture = glutils.load_texture(texture)

    def loadObject(self,program3d_id) :
        o = Object3D(self.vao, self.mesh.get_nb_triangles(), program3d_id, self.texture, self.tr)
        return o
