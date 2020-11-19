import math
import pygame as pg
from pygameUtils import rotate

CAR_HEIGHT = 100
CAR_WIDTH = 100
RADAR_COLOR = (0, 0, 255)


class Car(object):
    """Car class for pygame simulation"""

    def __init__(self, game_map):
        self.game_map = game_map
        self.surface = pg.image.load('red_car.png')
        self.surface = pg.transform.scale(
            self.surface, (CAR_WIDTH, CAR_HEIGHT)
        )
        self.rotate_surface = self.surface
        self.x_pos = 700
        self.y_pos = 650
        self.rect = [self.x_pos, self.y_pos]
        self.angle = 0
        self.speed = 1
        self.radars = []
        self.center = [
            self.x_pos + int(CAR_WIDTH/2), self.y_pos + int(CAR_HEIGHT/2)
        ]

    def draw(self, screen):
        """Renders the car intro the screen"""
        screen.blit(self.rotate_surface, [self.x_pos, self.y_pos])
        self.draw_radar(screen)

    def update(self, dif_x, dif_y, dif_angle):
        """Updates the car itself"""
        self.x_pos += dif_x
        self.y_pos += dif_y
        self.angle += dif_angle
        self.rotate_surface = rotate(self.surface, self.angle)

        # Draw the radars in the given angles
        for d in range(-90, 120, 45):
            self.update_radar(d)

    def update_radar(self, degree):
        """Updates the car radars and appends them to its list"""
        length = 0

        # Calculate the x center of the car, considering its rotation
        x_len = int(
            self.center[0] + math.cos(
                math.radians(360 - (self.angle + degree))
            ) * length
        )
        # Calculate the y center of the car, considering its rotation
        y_len = int(
            self.center[1] + math.sin(
                math.radians(360 - (self.angle + degree))
            ) * length
        )

        # We have to check if one of the sides is out of the track
        while not self.game_map.get_at((x_len, y_len)) == (255, 255, 255, 255) and length < 300:
            length += 100
            x_len = int(
                self.center[0] + math.cos(
                    math.radians(360 - (self.angle + degree))
                ) * length
            )

        # Get the vertical and horizontal side of the car
        horizontal = math.pow(x_len - self.center[0], 2)
        vertical = math.pow(y_len - self.center[1], 2)

        # If we get the hypotenuse of the triangle, we are also getting
        # the distance of the radar
        distance = int(math.sqrt(horizontal + vertical))
        self.radars.append([(x_len, y_len), distance])

    def draw_radar(self, screen):
        """Draws the radars on the screen"""
        for radar in self.radars:
            position, _ = radar
            pg.draw.line(screen, RADAR_COLOR, self.center, position, 1)
            pg.draw.circle(screen, RADAR_COLOR, position, 5)
