import logging
import pygame
import numpy as np

from typing import List


class Spritesheet:
    """
    Spritesheet

    This class handles loading spritesheets
    """

    @staticmethod
    def fully_slice_file(filename: str) -> List[List[pygame.Surface]]:
        """
        Fully slice surface by filename into an array of rows/columns

        :param filename: The filename to load
        """
        surface = pygame.image.load(filename)
        return Spritesheet.fully_slice(surface)

    @staticmethod
    def fully_slice(surface: pygame.Surface) -> List[List[pygame.Surface]]:
        """
        Fully slice a surface into an array of rows/columns

        :param surface: The surface to slice
        """
        sliced_sheet: List[List[pygame.Surface]] = []
        rows: List[pygame.Surface] = Spritesheet.slice_rows(surface)

        for row in rows:
            sliced_sheet.append(Spritesheet.slice_columns(row))

        return sliced_sheet

    @staticmethod
    def slice_rows(surface: pygame.Surface) -> List[pygame.Surface]:
        """
        Slice a surface into rows

        :param surface: The surface to slice
        """
        logger = logging.getLogger(__name__)

        logger.debug("Spritesheet beginning row slice")

        # Get the alpha of the spritesheet
        alphas = pygame.surfarray.pixels_alpha(surface)
        pixels = pygame.surfarray.array3d(surface)

        rows: List[pygame.Surface] = []

        region_start: int = None  # Where the region begins
        for i in range(0, alphas.shape[1]):
            row_alpha: int = np.sum(alphas[..., i])
            if row_alpha > 0 and region_start is None:
                region_start = i
                logger.debug(f"Spritesheet slicing region start index: {i}")
            elif row_alpha == 0 and region_start is not None:
                region_end = i - 1
                logger.debug(f"Spritesheet slicing region end index: {region_end}")

                row_surface: pygame.Surface = pygame.Surface.convert_alpha(
                    pygame.surfarray.make_surface(pixels[:, region_start:region_end])
                )
                surface_alpha_reference = pygame.surfarray.pixels_alpha(row_surface)
                np.copyto(surface_alpha_reference, alphas[:, region_start:region_end])
                del surface_alpha_reference  # Unlock the surface by removing the reference to alphas

                rows.append(row_surface)
                region_start = None

        logger.debug(f"Spritesheet sliced into {len(rows)} rows")
        return rows

    @staticmethod
    def slice_columns(surface: pygame.Surface) -> List[pygame.Surface]:
        """
        Slice surface into columns

        :param surface: The surface to slice
        """
        logger = logging.getLogger(__name__)

        logger.debug("Spritesheet beginning column slice")

        # Get the alpha of the spritesheet
        alphas = pygame.surfarray.pixels_alpha(surface)
        pixels = pygame.surfarray.array3d(surface)

        cols: List[pygame.Surface] = []

        region_start: int = None  # Where the region begins
        for i in range(0, alphas.shape[0]):
            row_alpha: int = np.sum(alphas[i])
            if row_alpha > 0 and region_start is None:
                region_start = i
                logger.debug(f"Spritesheet slicing region start index: {i}")
            elif row_alpha == 0 and region_start is not None:
                region_end = i - 1
                logger.debug(f"Spritesheet slicing region end index: {region_end}")

                row_surface: pygame.Surface = pygame.Surface.convert_alpha(
                    pygame.surfarray.make_surface(pixels[region_start:region_end, :])
                )
                surface_alpha_reference = pygame.surfarray.pixels_alpha(row_surface)
                np.copyto(surface_alpha_reference, alphas[region_start:region_end, :])
                del surface_alpha_reference  # Unlock the surface by removing the reference to alphas

                cols.append(row_surface)
                region_start = None

        logger.debug(f"Spritesheet sliced into {len(cols)} columns")
        return cols

