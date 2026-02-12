import time
import pygame
import numpy as np
import draw
import fisica



class Game:

    def __init__(self):

        self.physics_system = fisica.Physics_System()
        self.drawer = draw.Drawer((800, 600))

    def add_point(self, r, mass, radius, gravity=True, color=(255, 255, 255), visible=True):

        point =self.physics_system.add_point(r, mass, radius, gravity)
        if visible:
            self.drawer.points.append(point)
        return(point)

    def add_line(self, type, point1, point2, length=None, k=None, c=None, color=(255, 255, 255), visible=True):

        if length == None:
            length = np.linalg.norm(point1.r - point2.r)

        if type == "sd":
            joint = self.physics_system.add_spring_joint(point1, point2, length, k, c) 
        elif type == "f":
            joint = self.physics_system.add_fixed_joint(point1, point2, length)

        if visible:
            self.drawer.lines.append(joint)
        
        return(joint)

    def update(self, dt):

        self.physics_system.update(dt)
    
    def draw(self):

        self.drawer.draw()





########################################
Game = Game()

gravity = True

cabeza = Game.add_point(np.array([8, 4]), 5.0, 5, gravity=False)
pecho = Game.add_point(np.array([8, 3.9]), 20.0, 2, gravity=gravity)
pene = Game.add_point(np.array([8, 3.5]), 20.0, 2, gravity=gravity)
manod = Game.add_point(np.array([8.3, 3.6]), 5.0, 2, gravity=gravity)
manoi = Game.add_point(np.array([7.7, 3.6]), 5.0, 2, gravity=gravity)
pied = Game.add_point(np.array([8.2, 3.1]), 10.0, 2, gravity=gravity)
piei = Game.add_point(np.array([7.8, 3.1]), 10.0, 2, gravity=gravity)

cuello = Game.add_line("f", cabeza, pecho, None, 100000, 50)
torso = Game.add_line("f", pecho, pene, None, 100000, 50)
brazod = Game.add_line("f", pecho, manod, None, 100000, 50)
brazoi = Game.add_line("f", pecho, manoi, None, 100000, 50)
piernad = Game.add_line("f", pene, pied, None, 100000, 50)
piernai = Game.add_line("f", pene, piei, None, 100000, 50)
#Soporte
'''
Game.add_line(manod, manoi, False, 2000, 10, visible=False)
Game.add_line(pied, piei, False, 50000, 10, visible=False)
Game.add_line(manod, pied, False, 50000, 10, visible=False)
Game.add_line(manoi, piei, False, 50000, 10, visible=False)
Game.add_line(manod, pene, False, 2000, 10, visible=False)
Game.add_line(manoi, pene, False, 2000, 10, visible=False)
soporte1 = Game.add_point(np.array([8.2, 3.9]), 1, 1, gravity=False, visible=False)
soporte2 =Game.add_point(np.array([7.8, 3.9]), 1, 1, gravity=False, visible=False)
Game.add_line(cabeza, soporte1, False, 2000, 50, visible=False)
Game.add_line(cabeza, soporte2, False, 2000, 50, visible=False)
Game.add_line(pecho, soporte1, False, 2000, 50, visible=False)
Game.add_line(pecho, soporte2, False, 2000, 50, visible=False)
Game.add_line(pene, soporte1, False, 2000, 50, visible=False)
Game.add_line(pene, soporte2, False, 2000, 50, visible=False)
'''



########################################


running = True
mouse_button_down = False
while running:

    mouse_rel = np.array(pygame.mouse.get_rel())
    mouse_vel = mouse_rel / Game.drawer.zoom / 0.025
    mouse_vel = np.array([mouse_vel[0], -mouse_vel[1]])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down = True
            pecho.gravity = False
            pecho.v = np.array([0.0, 0.0])
        
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False
            pecho.gravity = True
            pecho.v = mouse_vel

    
    if mouse_button_down:
        mouse_pos = np.array(pygame.mouse.get_pos())
        world_pos_x = mouse_pos[0] / Game.drawer.zoom + Game.drawer.position[0]
        world_pos_y = (Game.drawer.window_size[1] - mouse_pos[1]) / Game.drawer.zoom + Game.drawer.position[1]
        dr = np.array([world_pos_x, world_pos_y]) - pecho.r
        pecho.r = pecho.r + dr


    Game.update(0.01)
    Game.draw()

    pygame.display.flip()
    time.sleep(0.01)
