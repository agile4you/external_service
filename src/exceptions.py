class BaseServiceException(Exception):
    def __init__(self, message, errors):

        super(BaseServiceException, self).__init__(message)

        self.errors = errors


class ServiceTypeException(ValueError):
    pass
