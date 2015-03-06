import traceback

class PsistatsException(BaseException):
    def __init__(self, message, cause=None):
        if (cause != None):
            message = message + ', caused by:' + "\n" + traceback.format_exc()

        super(PsistatsException, self).__init__(message)
        self.cause = cause

class ConfigException(PsistatsException):
    pass

class ConnectionException(PsistatsException):
    pass

class FileNotFoundException(PsistatsException):
    pass

class MessageNotSentException(PsistatsException):
    pass

class ExchangeException(PsistatsException):
    pass

class QueueException(PsistatsException):
    pass
