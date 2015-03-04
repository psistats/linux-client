import traceback

class PsistatsException(BaseException):
    def __init__(self, message, cause=None):
        if (cause != None):
            message = message + ', caused by:' + "\n" + traceback.format_exc()

        super(PsistatsException, self).__init__(message)
        self.cause = cause

class QueueConfigException(PsistatsException):
    pass

class QueueConnectionException(PsistatsException):
    pass

class FileNotFoundException(PsistatsException):
    pass

class MessageNotSentException(PsistatsException):
    pass
