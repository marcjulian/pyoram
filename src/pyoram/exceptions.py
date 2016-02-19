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
