APP_DATA = {
    "name": "Vengeance Pact",
    "version": "0.0.1",
    "clocks": {"logic": 100, "rendering": 60},
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_events_log_true": {"()": "settings.filters.SettingsFlag", "field": "events"},
        "require_not_keys_pressed": {"()": "settings.filters.NoKeysPressedFilter"},
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - [%(levelname)-7s - %(module)s (%(process)d %(thread)d)] %(name)s: %(message)s"
        },
        "simple": {"format": "%(asctime)s - [%(levelname)-7s - %(module)s] %(name)s: %(message)s"},
    },
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "simple"},},
    "root": {"handlers": ["console"], "level": "INFO", "formatter": "verbose",},
    "loggers": {
        "console": {"handlers": ["console"], "level": "INFO", "propagate": True,},
        "events.orchestrator": {"filters": ["require_events_log_true", "require_not_keys_pressed"]},
    },
}

SETTINGS = {"logging": {"events": False}}
