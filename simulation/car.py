import pygame as pg
from pygameUtils import rotate

CAR_HEIGHT = 100
CAR_WIDTH = 100


class Car:
    """Car class for pygame simulation"""

    def __init__(self):
        self.surface = pg.image.load('red_car.png')
        self.surface = pg.transform.scale(
            self.surface, (CAR_WIDTH, CAR_HEIGHT)
        )
        self.rotate_surface = self.surface
        self.x_pos = 500
        self.y_pos = 300
        self.rect = [self.x_pos, self.y_pos]
        self.angle = 0
        self.speed = 1
        self.center = [
            self.x_pos + int(CAR_WIDTH/2), self.y_pos + int(CAR_HEIGHT/2)
        ]

    def draw(self, screen):
        """Renders the car intro the screen"""
        screen.blit(self.rotate_surface, [self.x_pos, self.y_pos])

    def update(self, dif_x, dif_y, dif_angle):
        """Updates the car itself"""
        self.x_pos += dif_x
        self.y_pos += dif_y
        self.angle += dif_angle
        self.rotate_surface = rotate(self.surface, self.angle)
