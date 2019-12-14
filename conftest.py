import pytest
import pygame


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "freeze_time(timestamp): freeze time to the given timestamp for the duration of the test.",
    )

    pygame.init()
