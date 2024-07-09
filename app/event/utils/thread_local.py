"""
Basic thread-local functionality for working with request contexts
"""
from threading import local
from typing import Optional

from django.http.request import HttpRequest

REQUEST_THREAD_LOCAL = local()
REQUEST_THREAD_LOCAL.current_request = None


def reset_request_thread_local() -> local:
    """ Reset thread local """
    global REQUEST_THREAD_LOCAL  # pylint: disable=global-statement
    REQUEST_THREAD_LOCAL = local()
    REQUEST_THREAD_LOCAL.current_request = None
    REQUEST_THREAD_LOCAL.dirty_models = []
    return REQUEST_THREAD_LOCAL


def get_request_thread_local() -> local:
    """ Returns the shared thread local """
    return REQUEST_THREAD_LOCAL


def get_current_request() -> Optional[HttpRequest]:
    """ Returns the current request from the thread local """
    return REQUEST_THREAD_LOCAL.current_request if hasattr(REQUEST_THREAD_LOCAL, 'current_request') else None


def get_current_request_user():
    """ Returns the authenticated user for the current request """
    request = get_current_request()
    if request:
        # noinspection PyUnresolvedReferences
        return request.user
    return None
