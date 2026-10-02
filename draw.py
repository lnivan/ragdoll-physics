import numpy as np
import pygame




class Drawer:

    def __init__(self, window_size):
        pygame.init()
        self.window_size = window_size
        self.window = pygame.display.set_mode((window_size))
        self.points = []
        self.lines = []

        self.position = np.array([0.0, 0.0])
        self.zoom = 50.0

    def world_to_screen(self, world_pos):

        screen_x = int((world_pos[0] - self.position[0]) * self.zoom)
        screen_y = int(self.window_size[1] - (world_pos[1] - self.position[1]) * self.zoom)
        return(np.array([screen_x, screen_y]))


    def draw_point(self, point, color=(255, 255, 255)):

        pygame.draw.circle(self.window, color, self.world_to_screen(point.r), int(50*point.radius/self.zoom))

    def add_point(self, point):

        self.points.append(point)


    def draw_line(self, line, color=(255, 255, 255)):

        pygame.draw.line(self.window, color, self.world_to_screen(line.point1.r), self.world_to_screen(line.point2.r), 2)

    def add_line(self, line):

        self.lines.append(line)


    def draw(self):

        self.window.fill((0, 0, 0))

        for point in self.points:
            self.draw_point(point)

        for line in self.lines:
            self.draw_line(line)
    

