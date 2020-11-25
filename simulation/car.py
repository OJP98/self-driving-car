import math
import pygame as pg
from pygameUtils import rotate, calc_sides
from dotenv import load_dotenv
import os

CAR_HEIGHT = 100
CAR_WIDTH = 100
RADAR_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255, 255)
load_dotenv()


class Car(object):
    """Car class for pygame simulation"""

    def __init__(self, game_map):
        self.game_map = game_map
        self.surface = pg.image.load('red_car.png')
        self.surface = pg.transform.scale(
            self.surface, (CAR_WIDTH, CAR_HEIGHT)
        )
        self.rotate_surface = self.surface
        self.x_pos = 600
        self.y_pos = 655
        self.angle = 0
        self.speed = 7
        self.distance = 0
        self.collided = False
        self.collision_points = []
        self.radars = []
        self.center = [
            self.x_pos + 50, self.y_pos + 50
        ]

    def draw(self, screen):
        """Renders the car intro the screen"""
        screen.blit(self.rotate_surface, [self.x_pos, self.y_pos])
        self.draw_radar(screen)

    def update(self):
        """Updates the car itself"""
        #self.x_pos += dif_x
        #self.y_pos += dif_y
        self.distance += self.speed
        #self.angle += dif_angle
        self.x_pos += math.cos(math.radians(360-self.angle)) * self.speed
        self.y_pos += math.sin(math.radians(360-self.angle)) * self.speed
        self.center = [int(self.x_pos + 50), int(self.y_pos + 50)]
        self.rotate_surface = rotate(self.surface, self.angle)

        # Clear the radars that have been used
        self.update_collision_points()
        self.check_collision()
        self.radars.clear()

        sensoresList = []
        if (int(os.getenv("NUM_SENSORES")) == 3):
            sensoresList = list(range(-90, 120, 90))
        elif (int(os.getenv("NUM_SENSORES")) == 4):
            sensoresList = list(range(-90, 120, 60))
        elif (int(os.getenv("NUM_SENSORES")) == 5):
            sensoresList = list(range(-90, 120, 45))
        elif (int(os.getenv("NUM_SENSORES")) == 9):
            sensoresList = list(range(-90, 120, 25))
        elif (int(os.getenv("NUM_SENSORES")) == 11):
            sensoresList = list(range(-90, 120, 20))

        # Draw the radars in the given angles
        for degree in sensoresList:
            self.update_radar(degree)

    def update_radar(self, degree):
        """Updates the car radars and appends them to its list"""
        length = 0

        # Calculate the x center of the car, considering its rotation
        x_len = int(
            self.center[0] + math.cos(
                math.radians(360 - (self.angle + degree))
            ) * length
        )  # Calculate the y center of the car, considering its rotation
        y_len = int(
            self.center[1] + math.sin(
                math.radians(360 - (self.angle + degree))
            ) * length
        )

        # Check if the pixel we want is not out of range
        try:
            pixel = self.game_map.get_at((x_len, y_len))
        except IndexError:
            pixel = WHITE_COLOR

        # We have to check if one of the sides is out of the track
        while pixel != WHITE_COLOR and length < 300:

            try:
                # Try to get the furthest pixel in the game
                pixel = self.game_map.get_at((x_len, y_len))
            except IndexError:
                # If it fails, just set it as a white color
                pixel = WHITE_COLOR
            else:
                # Change the length and update x and y values
                length = length + 1

            # Update x values
            x_len = int(
                self.center[0] + math.cos(
                    math.radians(360 - (self.angle + degree))
                ) * length
            )

            # Update y values
            y_len = int(
                self.center[1] + math.sin(
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
        self.get_data()
        for radar in self.radars:
            position, _ = radar
            pg.draw.line(screen, RADAR_COLOR, self.center, position, 1)
            pg.draw.circle(screen, RADAR_COLOR, position, 2)

    def update_collision_points(self):
        """Calls for calc_sides method in order to get the sides of the car"""
        self.collision_points = calc_sides(self.center, self.angle)

    def check_collision(self):
        """Checks if one of the collision points of the car is a white pixel
            which if it is, means it got out of the track"""
        self.collided = False

        for point in self.collision_points:

            try:
                if self.game_map.get_at((
                    int(point[0]), int(point[1])
                )) == WHITE_COLOR:
                    self.collided = True
                    break
            except:
                self.collided = True

    def get_collided(self):
        """Returns if the car has collided or not"""
        return self.collided

    def get_reward(self):
        return self.distance/50.0

    def get_data(self):
        inputLayer = []
        for i in range(int(os.getenv("NUM_SENSORES"))):
            inputLayer.append(0)

        for i, radar in enumerate(self.radars):
            inputLayer[i] = int(radar[1]/30)
        return inputLayer
