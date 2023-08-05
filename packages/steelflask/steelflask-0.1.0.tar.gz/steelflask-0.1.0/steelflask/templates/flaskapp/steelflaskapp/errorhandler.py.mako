from flask import current_app
from werkzeug.exceptions import (MethodNotAllowed, NotFound, BadRequest)
from jwt.exceptions import InvalidSignatureError, DecodeError
from ${app_name}.exceptions import (ApiError)
from ${app_name}.ext import ResponseCode, ApiResponse


def handle_session_not_found_error(e):
    return ApiResponse.error(
        error_code=ResponseCode.AUTHENTICATION_REQUIRED,
        message="You need to login before performing this operation"
    )


def error_handler(*args, **kwargs):
    def handler_function(e):
        return ApiResponse.error(*args, **kwargs)

    return handler_function


def handle_api_error(e):
    return ApiResponse.error(
        error_code=e.error_code,
        errors=e.errors,
        message=e.message
    )


def handle_exception(e):
    current_app.logger.error(e)
    return ApiResponse.error(
        error_code=ResponseCode.UNKNOWN_ERROR,
        message='Some unknown error occured.'
    )


def register_error_handlers(app):
    app.register_error_handler(ApiError, handle_api_error)
    app.register_error_handler(InvalidSignatureError, handle_session_not_found_error)
    app.register_error_handler(DecodeError, handle_session_not_found_error)

    app.register_error_handler(BadRequest, error_handler(
        error_code=ResponseCode.BAD_REQUEST,
        message='Invalid input received.'))

    app.register_error_handler(NotFound, error_handler(
        error_code=ResponseCode.RESOURCE_NOT_FOUND,
        message='Not found'))

    app.register_error_handler(MethodNotAllowed, error_handler(
        error_code=ResponseCode.METHOD_NOT_ALLOWED,
        message='Method not allowed'))

    app.register_error_handler(Exception, handle_exception)
