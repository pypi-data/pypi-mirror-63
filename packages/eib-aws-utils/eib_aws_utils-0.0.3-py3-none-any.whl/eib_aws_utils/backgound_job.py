"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import logging

from eib_aws_utils.errors import EIBError

_logger = logging.getLogger(__name__)


def entry_point(func):
    def inner1(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except EIBError as error:
            _logger.log(error.log_level, f"[{error.title} ({error.http_status})] {error.detail}")
            raise error

        except Exception as error:
            _logger.exception(f"An unhandled exception occurs: {error}")
            raise error

    return inner1
