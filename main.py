from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
from pyrr import euler
from cactus import Cactus
from voiture import VoitureCourse, VoiturePolice
import random


def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1.5, 1.5, 1.5, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -3
    tr.rotation_center.z = 0.5
    texture = glutils.load_texture('stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = 5
    tr.translation.x = -4 
    rotation_angle = np.radians(180)
    tr.rotation_euler[2] += rotation_angle
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = 5
    tr.translation.x = 0 
    rotation_angle = np.radians(180)
    tr.rotation_euler[2] += rotation_angle
    texture = glutils.load_texture('stego_vert.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

 
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = 5
    tr.translation.x = -2 
    rotation_angle = np.radians(180)
    tr.rotation_euler[2] += rotation_angle
    texture = glutils.load_texture('stego_radio.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    m = Mesh.load_obj('skin.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2.5, 2.5, 2.5, 1]))
    tr = Transformation3D()
    tr.translation.y = 2.5
    tr.translation.z = 4.5
    tr.translation.x = -2
    tr.rotation_center.z = 0.5
    tr.rotation_euler = pyrr.euler.create(0, 0 , np.radians(180)) 
    texture = glutils.load_texture('rouge.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    m = Mesh.load_obj('drapeau.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1.5, 1.5, 1.5, 1]))
    tr = Transformation3D()
    tr.translation.y = 2
    tr.translation.z = -3
    tr.translation.x = -25
    tr.rotation_center.z = 0.5
    tr.rotation_euler = pyrr.euler.create(0, 0 , np.radians(90))  
    texture = glutils.load_texture('damier.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)


    nbr_Cactus_longueur = 16
    nbr_Cactus_largeur = 5
    nbr_Cactus_largeur2 = 7
    liste_Cactus = []
    texture = 'cactus.jpg'
    
    def create_cactus(id, texture, x, z, program3d_id):
        cactus = Cactus(id=id)
        cactus.Texture(texture)
        cactus.tr.translation.x = x
        cactus.tr.translation.z = z
        return cactus.loadObject(program3d_id)

    nbr_Cactus_longueur = 16
    nbr_Cactus_largeur = 5
    nbr_Cactus_largeur2 = 7
    liste_Cactus = []
    texture = 'cactus.jpg'

    # Créer les cactus le long de la longueur
    for i in range(nbr_Cactus_longueur):
        z = 7 if i < 5 else 0
        x = i * -1.2 + 1
        liste_Cactus.append(create_cactus(i, texture, x, z, program3d_id))

    for i in range(nbr_Cactus_longueur):
        x = i * -1.2 + 1
        z = -5.0
        liste_Cactus.append(create_cactus(nbr_Cactus_longueur + i, texture, x, z, program3d_id))

    # Créer les cactus le long de la largeur
    for i in range(nbr_Cactus_largeur):
        x = 2
        z = -i
        liste_Cactus.append(create_cactus(nbr_Cactus_longueur * 2 + i, texture, x, z, program3d_id))

    for i in range(nbr_Cactus_largeur2):
        x = 2
        z = -i + 7
        liste_Cactus.append(create_cactus(nbr_Cactus_longueur * 2 + nbr_Cactus_largeur + i, texture, x, z, program3d_id))

    for i in range(nbr_Cactus_largeur2):
        x = -5
        z = -i + 6
        liste_Cactus.append(create_cactus(nbr_Cactus_longueur * 2 + nbr_Cactus_largeur + nbr_Cactus_largeur2 + i, texture, x, z, program3d_id))


    for cactus in liste_Cactus:
        viewer.add_object(cactus)


    nrb_Voiture = 7
    listeVoiture = []
    texture1 ='police.png'
    texture2 = 'voiture_course.png'
    
    for i in range(2 * nrb_Voiture):
        random_number = random.randint(1,2)  
        if random_number == 1 :
            voiture = VoiturePolice(id=i % nrb_Voiture)
            voiture.Texture(texture1)
            
        else :
            voiture = VoitureCourse(id=i % nrb_Voiture)
            voiture.Texture(texture2)
            
        voiture.tr.translation.z = -30 - 9 * (i % nrb_Voiture)
        voiture.tr.translation.x = -20 if i < nrb_Voiture else -23
        listeVoiture.append(voiture.loadObject(program3d_id))

    
                            
    for voiture in listeVoiture :
        viewer.add_object(voiture)



    m = Mesh()
    p0, p1, p2, p3 = [-100, 0, -100], [100, 0, -100], [100, 0, 100], [-100, 0, 100]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    vao = Text.initialize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    level_text = Text('Niveau 1', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(level_text)
    viewer.level_text = level_text

    decompteur = Text('30', np.array([-0.3, 0.7], np.float32), np.array([0.1, 0.9], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(decompteur)
    viewer.decompteur = decompteur

    best_score = Text('Record :', np.array([-0.9, -0.9], np.float32), np.array([-0.1, -0.7], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(best_score)
    viewer.best_score = best_score


    viewer.run()


if __name__ == '__main__':
    main()