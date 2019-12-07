import pygame

from enum import Enum
from events.orchestrator import Orchestrator


class Event(Enum):
    TEST_MESSAGE = "event_test_message"
    KEYS_PRESSED = "event_keys_pressed"
