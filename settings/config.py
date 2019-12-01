APP_DATA = {
    'name': 'Vengeance Pact',
    'version': '0.0.1',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - [%(levelname)-7s - %(module)s (%(process)d %(thread)d)] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s - [%(levelname)-7s - %(module)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'formatter': 'verbose',
    },
    'loggers': {
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
