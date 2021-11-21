import sys

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default_formatter',
            'stream': sys.stderr
        },
    },

    'loggers': {
        'page_loader_logger': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
        }
    }
}
