class MiraiException(Exception):
    pass


class NetworkException(MiraiException):
    pass


class AuthenticationException(MiraiException):
    pass


class PrivilegeException(MiraiException):
    pass


class UnknownTargetException(MiraiException):
    pass


class BadRequestException(MiraiException):
    pass
