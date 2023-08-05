from ${app_name}.ext import ResponseCode


class ApiError(Exception):
    def __init__(self, error_code=ResponseCode.UNKNOWN_ERROR, errors=None, message="Some unknown error occured"):
        self.error_code = error_code
        self.errors = errors
        self.message = message


class ValidationError(ApiError):
    def __init__(self, errors=None, message='Invalid input received.'):
        self.error_code = ResponseCode.BAD_REQUEST
        self.errors = errors
        self.message = message
