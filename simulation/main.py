import sys
import pygame

# Constant variables
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
CAR_HEIGHT = 192
CAR_WIDTH = 112

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

# Car image with reescaling
carImg = pygame.image.load('red_car.png')
carImg = pygame.transform.scale(carImg, (
    int(CAR_WIDTH/2.5), int(CAR_HEIGHT/2.5)
))


def player(x_coord, y_coord):
    """Renders the player with its coordinates"""
    screen.blit(carImg, (x_coord, y_coord))


def main():
    """Main method for runing the pygame window"""
    # Initial x and y coords
    car_x = 370
    car_y = 0

    # Changing x and y coords
    car_x_change = 0
    car_y_change = 0

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
                    car_x_change = -0.1
                if event.key == pygame.K_RIGHT:
                    car_x_change = 0.1

                # Horizontal
                if event.key == pygame.K_DOWN:
                    car_y_change = -0.1
                if event.key == pygame.K_UP:
                    car_y_change = 0.1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    car_y_change = 0

        # set new coords
        car_y += car_y_change
        car_x += car_x_change

        # render car
        player(car_x, car_y)

        # update display
        pygame.display.update()


main()
sys.exit()
