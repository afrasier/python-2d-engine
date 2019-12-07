import pygame
import logging
import time

from imaging import Palette, KEY_HUES_LIST


def dev_palette():
    """
    Dev Demo function to demonstrate palette swaps
    """
    logger = logging.getLogger(__name__)
    logger.info("Running dev palette demo")

    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("test")

    image = pygame.image.load("assets/testing/img/ball.jpg")
    simple_image = pygame.image.load("assets/testing/img/ball_simple.jpg")
    complex_image = pygame.image.load("assets/testing/img/ball_complex.jpg")
    trans_image = pygame.image.load("assets/testing/img/ball_transparent.png")
    mage_image = pygame.image.load("assets/testing/img/mage_ss.png")
    newHues = {240: 0, 200: 64, 160: 44, 100: 305}

    palette = Palette(newHues)
    new_image = palette.paint_image(image)
    new_simple_image = palette.paint_image(simple_image)
    new_complex_image = palette.paint_image(complex_image)
    new_trans_image = palette.paint_image(trans_image)
    new_mage_image = palette.paint_image(mage_image)

    # Full red
    red_hues = {i: 0 for i in range(0, 360)}
    palette_red = Palette(red_hues, tolerance=0)
    button_image = pygame.image.load("assets/testing/img/button_test.png")
    new_button_image = palette_red.paint_image(button_image)

    screen.blit(simple_image, (0, 0))
    screen.blit(new_simple_image, (101, 0))
    screen.blit(image, (0, 101))
    screen.blit(new_image, (101, 101))
    screen.blit(complex_image, (0, 202))
    screen.blit(new_complex_image, (101, 202))
    screen.blit(trans_image, (0, 303))
    screen.blit(new_trans_image, (101, 303))
    screen.blit(mage_image, (0, 404))
    screen.blit(new_mage_image, (201, 404))

    screen.blit(button_image, (200, 0))
    screen.blit(new_button_image, (301, 0))
    pygame.display.flip()

    time.sleep(10)
