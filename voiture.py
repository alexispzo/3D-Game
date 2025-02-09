import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

class Voiture:
    def __init__(self, id, objet):
        self.id = id
        self.mesh = Mesh.load_obj(objet)
        self.mesh.normalize()
        self.mesh.apply_matrix(pyrr.matrix44.create_from_scale([1.3, 1.3, 1.3, 1.3]))
        self.tr = Transformation3D()

        self.tr.translation.y = -np.amin(self.mesh.vertices, axis=0)[1]
        self.tr.rotation_center.z = 0.5
        rotation_matrix = pyrr.matrix44.create_from_y_rotation(np.radians(45))
        self.tr.rotation = rotation_matrix
        self.vao = self.mesh.load_to_gpu()

    def Texture(self, texture):
        self.texture = glutils.load_texture(texture)

    def loadObject(self, program3d_id):
        return Object3D(self.vao, self.mesh.get_nb_triangles(), program3d_id, self.texture, self.tr)
    
class VoiturePolice(Voiture):
    def __init__(self, id):
        super().__init__(id, 'police.obj')


class VoitureCourse(Voiture):
    def __init__(self, id):
        super().__init__(id, 'voiture_course.obj')



        