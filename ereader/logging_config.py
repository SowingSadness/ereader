MAX_LOG_SIZE = 10 * 1024 * 1024

DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)-7s  %(asctime)s %(module)s'
                       ' %(process)d %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)-7s %(asctime)s %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        #'file': {
        #    'level': 'DEBUG',
        #    'filename': 'ereader.log',
        #    'class': 'logging.handlers.RotatingFileHandler',
        #    'formatter': 'simple',
        #    'maxBytes': MAX_LOG_SIZE,
        #}
    },
    'loggers': {
        'ereader': {
            'handlers': ['console', ],
        },
        'ereader.plugin': {
            'propagate': False,
            'handlers': ['console', ],
        },
        'ereader.readers.CommonReader': {
            'propagate': False,
            'handlers': ['console', ],
        },
        #'ereader.runner': {
        #    'handlers': ['file', ],
        #},
    }
}
