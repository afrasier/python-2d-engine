import pygame
import argparse
import logging
import logging.config
import time
from settings import config
from imaging.palette import Palette

from events import Orchestrator, Event

'''
VENGEANCE PACT 

A Darkest Dungeon-like game inspired by the Stormlight Archive by Brandon Sanders
'''

'''
The main method handles initial configurations and parses any command line arguments
'''
class Test():
    def print_it(self, x):
        print(f"{x}, for sure!")

def main():
    # Set up our argument parser for handing command line options
    parser = argparse.ArgumentParser(description=f"{config.APP_DATA.get('name')} - v{config.APP_DATA.get('version')}")
    parser.add_argument('-ll', '--log-level', help="Set the default log level")

    args = parser.parse_args()

    print(args)

    print(f"Starting {config.APP_DATA.get('name')} v{config.APP_DATA.get('version')}...")

    logging.config.dictConfig(config.LOGGING)
    logger = logging.getLogger() # Use __name__ in subpackages

    logger.info("Configured logger")

    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('test')

    image = pygame.image.load('assets/testing/img/ball.jpg')
    simple_image = pygame.image.load('assets/testing/img/ball_simple.jpg')
    complex_image = pygame.image.load('assets/testing/img/ball_complex.jpg')
    trans_image = pygame.image.load('assets/testing/img/ball_transparent.png')
    newHues = [0, 68, 44, 305]

    palette = Palette(newHues)
    new_image = palette.paint_image(image)
    new_simple_image = palette.paint_image(simple_image)
    new_complex_image = palette.paint_image(complex_image)
    new_trans_image = palette.paint_image(trans_image)

    screen.blit(simple_image, (0, 0))
    screen.blit(new_simple_image, (101, 0))
    screen.blit(image, (0, 101))
    screen.blit(new_image, (101, 101))
    screen.blit(complex_image, (0, 202))
    screen.blit(new_complex_image, (101, 202))
    screen.blit(trans_image, (0, 303))
    screen.blit(new_trans_image, (101, 303))
    pygame.display.flip()

    time.sleep(10)



if __name__ == "__main__":
    main()
