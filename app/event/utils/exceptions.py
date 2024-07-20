import traceback
import logging

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from . import constants
from .. import logger

response_logger = logging.getLogger(settings.BX_LOGGER)


def core_exception_handler(exc, context):
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)
    handlers = {
        'AuthenticationFailed': _handle_auth_error_error,
        'UserDeactivated': _handle_custom_exception,
        "CustomException": _handle_custom_exception,
        'UserSaveError': _handle_user_save_error,
    }
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_auth_error_error(exc, context, response):
    response.status_code = 401  # setting response code as 401
    response.data = {'errors': response.data}

    return response


def _handle_user_save_error(exc, context, response):
    from rest_framework.views import set_rollback
    data = {'detail': exc.args[0]}
    set_rollback()
    return Response(data, status=exc.status_code)


def _handle_custom_exception(exc, context, response):
    from rest_framework.views import set_rollback
    """
    :param exc: CustomExceptionClass
        Exception object
    :param context: dict
        API context
    :param response:
    :return: Response object
        {"message": <str>, status_code: <int>}
    """
    kwargs = exc.kwargs
    if exc.log_msg:
        logger.error(exc.log_msg)
    else:
        logger.error(constants.DEFAULT_ERROR_MESSAGE)
    response = {}
    for k, v in kwargs.items():
        response[k] = v

    if not response:
        response = {"message": constants.DEFAULT_ERROR_MESSAGE}

    set_rollback()
    return Response(response, status=exc.status)


class CustomException(Exception):
    """ Base class for handling custom exceptions """
    status = HTTP_400_BAD_REQUEST

    def __init__(self, *args, **kwargs):
        """
        :param args: tuple
            (custom exception message (first value), parameters to be replaced inside the custom message(n values)
        :param kwargs: dict
            keyword arguments. Ex: custom status_code
        """
        self.status = kwargs.get("status", self.status)
        self.log_msg = kwargs.get("log_msg")
        response_logger.info(traceback.format_exc())
        if kwargs:
            kwargs.pop("status", None)
            kwargs.pop("log_msg", None)
        self.kwargs = kwargs


class UserSaveError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message, **kwargs):
        self.status = self.status_code
        self.log_msg = message
        self.kwargs = kwargs
        response_logger.info(traceback.format_exc())

    def __str__(self):
        return repr(self.status_code)


class UserDeactivated(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message, **kwargs):
        self.status = self.status_code
        self.log_msg = message
        self.kwargs = kwargs
        response_logger.info(traceback.format_exc())

    def __str__(self):
        return repr(self.status_code)
