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
            self.drawer.points.append(self.physics_system.points[-1])
        return(point)

    def add_line(self, point1, point2, rest_length=False, k=1000, c=10, color=(255, 255, 255), visible=True):

        if not rest_length:
            rest_length = np.linalg.norm(point1.r - point2.r)
        
        joint =self.physics_system.add_spring_damper_joint(point1, point2, rest_length, k, c)
        if visible:
            self.drawer.lines.append(self.physics_system.joints[-1])
        return(joint)

    def update(self, dt):

        self.physics_system.update(dt)
    
    def draw(self):

        self.drawer.draw()





########################################
Game = Game()

gravity = True

cabeza = Game.add_point(np.array([8, 4]), 4.0, 5, gravity=False)
pecho = Game.add_point(np.array([8, 3.9]), 20.0, 2, gravity=gravity)
pene = Game.add_point(np.array([8, 3.5]), 20.0, 2, gravity=gravity)
manod = Game.add_point(np.array([8.3, 3.6]), 5.0, 2, gravity=gravity)
manoi = Game.add_point(np.array([7.7, 3.6]), 5.0, 2, gravity=gravity)
pied = Game.add_point(np.array([8.2, 3.1]), 10.0, 2, gravity=gravity)
piei = Game.add_point(np.array([7.8, 3.1]), 10.0, 2, gravity=gravity)

cuello = Game.add_line(cabeza, pecho, False, 10000, 100)
torso = Game.add_line(pecho, pene, False, 10000, 100)
brazod = Game.add_line(pecho, manod, False, 10000, 100)
brazoi = Game.add_line(pecho, manoi, False, 10000, 100)
piernad = Game.add_line(pene, pied, False, 10000, 100)
piernai = Game.add_line(pene, piei, False, 10000, 100)
#Soporte
Game.add_line(manod, manoi, False, 1000, 10, visible=False)
Game.add_line(pied, piei, False, 1000, 10, visible=False)
Game.add_line(manod, pied, False, 1000, 10, visible=False)
Game.add_line(manoi, piei, False, 1000, 10, visible=False)
Game.add_line(manod, pene, False, 1000, 10, visible=False)
Game.add_line(manoi, pene, False, 1000, 10, visible=False)

soporte1 = Game.add_point(np.array([8.1, 3.9]), 1, 1, gravity=False, visible=False)
soporte2 =Game.add_point(np.array([7.9, 3.9]), 1, 1, gravity=False, visible=False)
Game.add_line(cabeza, soporte1, False, 5000, 100, visible=False)
Game.add_line(cabeza, soporte2, False, 5000, 100, visible=False)
Game.add_line(pecho, soporte1, False, 10000, 100, visible=False)
Game.add_line(pecho, soporte2, False, 10000, 100, visible=False)
Game.add_line(pene, soporte1, False, 10000, 100, visible=False)
Game.add_line(pene, soporte2, False, 10000, 100, visible=False)




########################################


running = True
mouse_button_down = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False
    
    if mouse_button_down:
        mouse_pos = np.array(pygame.mouse.get_pos())
        world_pos_x = mouse_pos[0] / Game.drawer.zoom + Game.drawer.position[0]
        world_pos_y = (Game.drawer.window_size[1] - mouse_pos[1]) / Game.drawer.zoom + Game.drawer.position[1]
        pecho.r = np.array([world_pos_x, world_pos_y])
        pecho.v = np.array([0.0, 0.0])

    Game.update(0.01)
    Game.draw()

    pygame.display.flip()
    time.sleep(0.01)
