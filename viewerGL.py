#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
import glutils
import random




class ViewerGL:
    def __init__(self):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(1600, 1100, 'OpenGL', None, None)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")
        self.objs = []
        self.touch = {}
        self.niveau = 1
        self.best_niveau = 1
        self.decompteur = 30
        self.decompteur_value = int(self.decompteur)
        self.last_time = glfw.get_time()


    def add_object(self, obj):
        self.objs.append(obj)

    def update_level_text(self):
        self.level_text.update_text(f'Niveau {self.niveau}')
    
    def update_best_score(self) :
        self.best_score.update_text(f'Record : Niveau {self.best_niveau}')

    def update_decompteur(self) :
        current_time = glfw.get_time()
        elapsed_time = current_time - self.last_time
        if elapsed_time >= 1.0:
            self.decompteur_value -= 1
            self.decompteur.update_text(f'{self.decompteur_value}')
            self.last_time = current_time

    def reset_game(self, init_stego_pos) :
        self.niveau = 1
        self.decompteur_value = 30
        self.update_level_text()
        self.decompteur.update_text(f'{self.decompteur_value}')
        self.objs[0].transformation.translation = init_stego_pos

    def change_skin(self, texture):
        new_texture = glutils.load_texture(texture)
        self.objs[0].texture = new_texture

    def future_position_valable(self, future_pos):
        for obj in self.objs[6:57]:
                d = future_pos - obj.transformation.translation
                distance = pyrr.vector.squared_length(d)
                
                if distance < 0.5 :
                    return False
                
        return True


    

    def run(self):
        while not glfw.window_should_close(self.window):
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            
            stegosaurus = self.objs[0]

            future_position = self.objs[0].transformation.translation
            if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
                future_position = self.objs[0].transformation.translation + pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), 
                                                                                                          pyrr.Vector3([0, 0, 0.08]))

            elif glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
                future_position = self.objs[0].transformation.translation - pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.08]))
            
            if self.future_position_valable(future_position) :
                stegosaurus.transformation.translation = future_position

            
            self.update_key_camera()

            for obj in self.objs[57:71] :
                d2 = stegosaurus.transformation.translation - obj.transformation.translation 
                d = pyrr.vector.squared_length(d2)
                if d < 1 :
                    self.reset_game(init_stego_pos)
                    
            if self.decompteur_value == 0 :
                self.reset_game(init_stego_pos)


            target_position = 20
            def mouvement(niv):
                for i, obj in enumerate(self.objs[57:71]):
                    if i <= 7:
                        initial_position = pyrr.Vector3([-20, 0.55, -30 - 9 * i])
                        obj.transformation.translation += pyrr.matrix33.apply_to_vector(
                            pyrr.matrix33.create_from_eulers(self.objs[3].transformation.rotation_euler),
                            pyrr.Vector3([0, 0, -0.05 * niv * random.randint(1, 4)])
                        )
                        if (target_position - obj.transformation.translation[2]) < 0.01:
                            obj.transformation.translation = initial_position
                    else:
                        initial_position = pyrr.Vector3([-23, 0.55, -30 - 9 * i])
                        obj.transformation.translation += pyrr.matrix33.apply_to_vector(
                            pyrr.matrix33.create_from_eulers(self.objs[3].transformation.rotation_euler),
                            pyrr.Vector3([0, 0, -0.05 * niv * random.randint(1, 4)])
                        )
                        if (target_position - obj.transformation.translation[2]) < 0.01:
                            obj.transformation.translation = initial_position

            mouvement(self.niveau)

            init_stego_pos = pyrr.Vector3([0, 0.73741776, -3])
            if self.objs[0].transformation.translation[0] < -25.5:
                self.objs[0].transformation.translation = init_stego_pos
                self.niveau += 1
                self.decompteur_value = 30
                self.update_decompteur()
                self.update_level_text()

            
            if pyrr.vector.squared_length(self.objs[0].transformation.translation - self.objs[3].transformation.translation) < 2:
                self.change_skin('stego_radio.png')
            if pyrr.vector.squared_length(self.objs[0].transformation.translation - self.objs[1].transformation.translation) < 2 :
                self.change_skin('stegosaurus.jpg')            
            if pyrr.vector.squared_length(self.objs[0].transformation.translation - self.objs[2].transformation.translation) < 2:
                self.change_skin('stego_vert.png')

          

            self.update_decompteur()
            self.update_best_score()

            if self.niveau > self.best_niveau :
                self.best_niveau = self.niveau
                self.update_best_score

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.touch[key] = 1
        elif action == glfw.RELEASE:
            self.touch[key] = 0
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key_avant(self):  
            if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
                    
                    self.objs[0].transformation.translation += \
                        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.08]))
    
    def update_key_arriere(self):  
        
            if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
               
                self.objs[0].transformation.translation -= \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.08]))

    def update_key_camera(self):    
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.02
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.02


        
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])
