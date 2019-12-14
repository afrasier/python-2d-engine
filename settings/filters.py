import logging

from settings.config import SETTINGS


class SettingsFlag(logging.Filter):
    def __init__(self, field: str):
        self.field = field

    def filter(self, rec):
        return SETTINGS.get("logging", {}).get(self.field, False)


class NoKeysPressedFilter(logging.Filter):
    def filter(self, rec):
        return "Event.KEYS_PRESSED" not in rec.msg
