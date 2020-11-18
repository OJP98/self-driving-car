import sys
import pygame
from car import Car

# Constant variables
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
CAR_HEIGHT = 192
CAR_WIDTH = 112
GENERATION = 0

# Initialize the game
pygame.init()

# Initial screen values
screen = pygame.display.set_mode((
    SCREEN_HEIGHT, SCREEN_WIDTH
))

# Window display settings
pygame.display.set_caption('Self Driving Car!')
icon = pygame.image.load('red_car.png')
pygame.display.set_icon(icon)


def main():
    """Main method for runing the pygame window"""

    car = Car()

    dif_x = 0
    dif_y = 0
    dif_angle = 0

    running = True
    while running:
        # RGB - Red, Green, Blue
        screen.fill((40, 40, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keystrokes (up, down, left and right)
            if event.type == pygame.KEYDOWN:
                # Vertical
                if event.key == pygame.K_LEFT:
                    dif_x = -0.1
                if event.key == pygame.K_RIGHT:
                    dif_x = 0.1

                # Horizontal
                if event.key == pygame.K_DOWN:
                    dif_y = 0.1
                if event.key == pygame.K_UP:
                    dif_y = -0.1

                if event.key == pygame.K_SPACE:
                    dif_angle = 0.1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dif_x = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    dif_y = 0

                if event.key == pygame.K_SPACE:
                    dif_angle = 0

        # Update car methods
        car.update(dif_x, dif_y, dif_angle)
        car.draw(screen)

        # update display
        pygame.display.update()


main()
sys.exit()
