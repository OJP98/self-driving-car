import sys
import pygame
from car import Car
import neat
from dotenv import load_dotenv
import os

# Constant variables
SCREEN_HEIGHT = 1500
SCREEN_WIDTH = 800
CAR_HEIGHT = 192
CAR_WIDTH = 112
GENERATION = 0

load_dotenv()

# Window display settings
pygame.display.set_caption('Self Driving Car!')
icon = pygame.image.load('red_car.png')
pygame.display.set_icon(icon)

# Map to be tested
env_map = os.getenv('MAP')

if env_map == '1':
    game_map = pygame.image.load('practice_track.png')
elif env_map == '2':
    game_map = pygame.image.load('track1.png')
elif env_map == '3':
    game_map = pygame.image.load('track2.png')
else:
    game_map = pygame.image.load('practice_track.png')


def main():
    """Main method for runing the pygame window"""

    car = Car(game_map)

    dif_x = 0
    dif_y = 0
    dif_angle = 0
    car_speed = 6

    running = True
    while running:
        # RGB - Red, Green, Blue
        # screen.fill((40, 40, 40))
        screen.blit(game_map, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keystrokes (up, down, left and right)
            if event.type == pygame.KEYDOWN:
                # Vertical
                if event.key == pygame.K_LEFT:
                    #dif_x = -car_speed
                    dif_angle = -car_speed
                if event.key == pygame.K_RIGHT:
                    #dif_x = car_speed
                    dif_angle = car_speed

                # Horizontal
                if event.key == pygame.K_DOWN:
                    dif_y = car_speed
                if event.key == pygame.K_UP:
                    dif_y = -car_speed

                if event.key == pygame.K_SPACE:
                    dif_angle = car_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dif_x = 0
                    dif_angle = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    dif_y = 0

                if event.key == pygame.K_SPACE:
                    dif_angle = 0

        # Update car methods
        car.update(dif_x, dif_y, dif_angle)

        if not car.get_collided():
            car.draw(screen)

        # update display
        pygame.display.update()


def run_car(genomes, config):

    # Init NEAT
    nets = []
    cars = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        # Init my cars
        cars.append(Car(game_map))

    # Init my game
    pygame.init()
    screen = pygame.display.set_mode((
        SCREEN_HEIGHT, SCREEN_WIDTH
    ))

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 70)
    font = pygame.font.SysFont("Arial", 30)
    #map = pygame.image.load('map.png')

    # Main loop
    global GENERATION
    GENERATION += 1
    while True:
        screen.blit(game_map, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # Input my data and get result from network
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_data())
            i = output.index(max(output))
            if i == 0:
                car.angle += 10
            else:
                car.angle -= 10

        # Update car and fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if not(car.get_collided()):
                remain_cars += 1
                car.update()
                genomes[i][1].fitness += car.get_reward()

        # check
        if remain_cars == 0:
            break

        # Drawing
        screen.blit(game_map, (0, 0))
        for car in cars:
            if not(car.get_collided()):
                car.draw(screen)

        text = generation_font.render(
            "Generation : " + str(GENERATION), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH + 300, 150)
        screen.blit(text, text_rect)

        text = font.render("Remain cars : " +
                           str(remain_cars), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH + 300, 200)
        screen.blit(text, text_rect)

        text = font.render("Number of sensors : " +
                           str(os.getenv("NUM_SENSORES")), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH + 300, 230)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(0)


if __name__ == "__main__":
    # Set configuration file
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(run_car, 1000)
