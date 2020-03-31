class AppException(Exception):
    status_code = 500
    message_code = 'InternalError'
    message_human = ''

    def __init__(self, message='', data=None):
        super().__init__(message)
        self.message = message
        self.data = data


class InvalidData(AppException):
    status_code = 400
    message_code = 'InvalidData'


class Unauthorized(AppException):
    status_code = 401
    message_code = 'Unauthorized'
