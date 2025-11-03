class ApplicationException(Exception):
    pass


class NotFoundException(ApplicationException):
    pass


class ConflictException(ApplicationException):
    pass


class NotAuthenticatedException(ApplicationException):
    pass


class VendorAlreadyRegisteredException(ConflictException):
    pass
