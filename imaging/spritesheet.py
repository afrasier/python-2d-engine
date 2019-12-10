import pygame
import logging
import numpy as np

from typing import List


class Spritesheet:
    """
    Spritesheet

    This class handles loading spritesheets
    """

    def __init__(self, file: str):
        self.logger = logging.getLogger(__name__)
        self.spritesheet: pygame.Surface = pygame.image.load(file)

    def slice_rows(self) -> List[pygame.Surface]:
        """
        Slice a sprite sheet into rows by scanning each row for alpha values
        """
        self.logger.debug("Spritesheet beginning row slice")

        # Get the alpha of the spritesheet
        alphas = pygame.surfarray.pixels_alpha(self.spritesheet)
        pixels = pygame.surfarray.array3d(self.spritesheet)

        rows: List[pygame.Surface] = []

        region_start: int = None  # Where the region begins
        for i in range(0, alphas.shape[1]):
            row_alpha: int = np.sum(alphas[..., i])
            if row_alpha > 0 and region_start is None:
                region_start = i
                self.logger.debug(f"Spritesheet slicing region start index: {i}")
            elif row_alpha == 0 and region_start is not None:
                region_end = i - 1
                self.logger.debug(f"Spritesheet slicing region end index: {region_end}")

                row_surface: pygame.Surface = pygame.Surface.convert_alpha(
                    pygame.surfarray.make_surface(pixels[:, region_start:region_end])
                )
                surface_alpha_reference = pygame.surfarray.pixels_alpha(row_surface)
                np.copyto(surface_alpha_reference, alphas[:, region_start:region_end])
                del surface_alpha_reference  # Unlock the surface by removing the reference to alphas

                rows.append(row_surface)
                region_start = None

        self.logger.debug(f"Spritesheet sliced into {len(rows)} rows")

