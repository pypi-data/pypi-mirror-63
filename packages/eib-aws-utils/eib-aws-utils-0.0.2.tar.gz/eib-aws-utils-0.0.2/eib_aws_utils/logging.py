"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import logging
import logging.config
import os

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    context = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs:
            print(kwargs['context'])
            self.aws_request_id = getattr(kwargs['context'], 'aws_request_id', None)
        else:
            self.aws_request_id = None

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if self.context is not None:
            log_record['aws_request_id'] = getattr(self.context, 'aws_request_id', None)


def configure_logging(main_module_name, context):
    logging.config.dictConfig(_get_default_logging_config(main_module_name))
    CustomJsonFormatter.context = context


def _get_default_logging_config(main_module_name):
    return {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'DEBUG'
            },
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s %(name)s %(levelname)s %(lineno)s %(module)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z',
                'class': 'eib_aws_utils.logging.CustomJsonFormatter'
            }
        },
        'disable_existing_loggers': False,
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'loggers': {
            main_module_name: {
                'level': os.getenv('LOGGING_LEVEL', 'INFO')
            }
        }
    }
