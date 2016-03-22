class WrongPassword(Exception):
    def __init__(self, message, reason=None):
        super(WrongPassword, self).__init__(message)
        self._reason = reason


class ErrorInKeyMap(Exception):
    def __init__(self, message, reason=None):
        super(ErrorInKeyMap, self).__init__(message)
        self._reason = reason


class ErrorInCloudMap(Exception):
    def __init__(self, message, reason=None):
        super(ErrorInCloudMap, self).__init__(message)
        self._reason = reason


class NoSelectedNode(Exception):
    def __init__(self, message, reason=None):
        super(NoSelectedNode, self).__init__(message)
        self._reason = reason


class DownloadFileError(Exception):
    def __init__(self, message, reason=None):
        super(DownloadFileError, self).__init__(message)
        self._reason = reason


class FileSizeError(Exception):
    def __init__(self, message, reason=None):
        super(FileSizeError, self).__init__(message)
        self._reason = reason


class DummyFileFound(Exception):
    pass
