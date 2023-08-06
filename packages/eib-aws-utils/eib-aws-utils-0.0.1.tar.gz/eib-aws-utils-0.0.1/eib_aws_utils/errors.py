"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import logging


class EIBError(Exception):
    log_level = logging.ERROR
    title = None
    http_status = 500

    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail


class BackendError(EIBError):
    title = 'API Internal Error'


class ClientError(EIBError):
    log_level = logging.WARNING
    title = "API Error"
    http_status = 400

    def __init__(self, detail, http_status=None, title=None):
        super().__init__(detail)
        if http_status is not None:
            self.http_status = http_status

        if title is not None:
            self.title = title


class BadRequestError(ClientError):
    TITLE = 'Bad Request'
    HTTP_STATUS = 400


class NotFoundError(ClientError):
    TITLE = 'Not Found'
    HTTP_STATUS = 404
