class Error(Exception):
    def __init__(self, message):
        self.message = message


class ValidationError(Error):
    def __init__(self, message):
        super().__init__(message)


class ProcessError(Error):
    def __init__(self, message):
        super().__init__(message)


class NotYetImplementedError(Error):
    def __init__(self, message):
        super().__init__(message)
