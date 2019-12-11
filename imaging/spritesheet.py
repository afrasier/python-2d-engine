import logging
import pygame
import numpy as np

from enum import Enum
from typing import List


class Spritesheet:
    """
    Spritesheet

    This class handles loading spritesheets
    """

    BREAK_COEFFICIENT_TRANSPARENT: int = 0
    BREAK_COEFFICIENT_SOLID: int = 255

    @staticmethod
    def fully_slice_file(filename: str, break_coefficient: int) -> List[List[pygame.Surface]]:
        """
        Fully slice surface by filename into an array of rows/columns

        :param filename: The filename to load
        :param break_coefficient: The break coefficient for slicing
        """
        surface = pygame.image.load(filename)
        return Spritesheet.fully_slice(surface, break_coefficient)

    @staticmethod
    def fully_slice(surface: pygame.Surface, break_coefficient: int) -> List[List[pygame.Surface]]:
        """
        Fully slice a surface into an array of rows/columns

        :param surface: The surface to slice
        :param break_coefficient: The break coefficient for slicing
        """
        sliced_sheet: List[List[pygame.Surface]] = []
        rows: List[pygame.Surface] = Spritesheet.slice_rows(surface, break_coefficient)

        for row in rows:
            sliced_sheet.append(Spritesheet.slice_columns(row, break_coefficient))

        return sliced_sheet

    @staticmethod
    def slice_by(surface: pygame.Surface, break_coefficient: int, by_cols: bool = False) -> List[pygame.Surface]:
        """
        Slice a surface into rows

        :param surface: The surface to slice
        :param break_coefficient: The break coefficient for slicing
        :param by_cols: Slice by columns instead of rows
        """
        logger = logging.getLogger(__name__)
        directionality: str = "rows"
        if by_cols:
            directionality = "columns"

        logger.debug(f"Spritesheet beginning {directionality} slice")

        # Get the alpha of the spritesheet
        alphas = pygame.surfarray.pixels_alpha(surface)
        pixels = pygame.surfarray.array3d(surface)

        slices: List[pygame.Surface] = []

        region_start: int = 0  # Where the region begins
        region_end: int = None

        shape = alphas.shape[1]
        if by_cols:
            shape = alphas.shape[0]

        for i in range(0, shape):
            subarray = None
            if by_cols:
                subarray = alphas[i]
            else:
                subarray = alphas[..., i]

            row_alpha: int = np.sum(subarray)
            target_alpha: int = subarray.shape[0] * break_coefficient

            if row_alpha == target_alpha:
                # We are on a "break line"
                if region_start == i:
                    # We've only moved 1 line down, i.e. in a "break block"
                    region_start = i + 1  # Our image begins on the NEXT line
                else:
                    # We're on a line >1 away from our region start, so our intervening lines are our image
                    region_end = i - 1

                if region_end is not None:
                    # We've identified a start and end region
                    logger.debug(f"Slicing region ({directionality}): {region_start} to {region_end}")
                    new_alphas = None
                    if by_cols:
                        new_alphas = alphas[region_start:region_end]
                    else:
                        new_alphas = alphas[:, region_start:region_end]

                    # Check they're not all transparent
                    if np.sum(new_alphas) == 0:
                        logger.debug(f"Region is empty, skipping...")
                    else:
                        new_pixels = None
                        if by_cols:
                            new_pixels = pixels[region_start:region_end]
                        else:
                            new_pixels = pixels[:, region_start:region_end]

                        row_surface: pygame.Surface = pygame.Surface.convert_alpha(
                            pygame.surfarray.make_surface(new_pixels)
                        )
                        surface_alpha_reference = pygame.surfarray.pixels_alpha(row_surface)
                        np.copyto(surface_alpha_reference, new_alphas)
                        del surface_alpha_reference  # Unlock the surface by removing the reference to alphas

                        slices.append(row_surface)

                    region_start = region_end + 2  # +1 to get to the break line, +1 to jump to next viable region
                    region_end = None

        logger.info(f"Spritesheet sliced into {len(slices)} {directionality}")
        return slices

    @staticmethod
    def slice_rows(surface: pygame.Surface, break_coefficient: int) -> List[pygame.Surface]:
        """
        Slice a surface into rows

        :param surface: The surface to slice
        :param break_coefficient: The break coefficient for slicing
        """
        return Spritesheet.slice_by(surface, break_coefficient)

    @staticmethod
    def slice_columns(surface: pygame.Surface, break_coefficient: int) -> List[pygame.Surface]:
        """
        Slice surface into columns

        :param surface: The surface to slice
        :param break_coefficient: The break coefficient for slicing
        """
        return Spritesheet.slice_by(surface, break_coefficient, by_cols=True)
