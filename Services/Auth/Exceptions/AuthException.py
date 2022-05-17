class AuthException(Exception):
    pass


class AuthDBException(AuthException):
    pass


class LoginExists(AuthDBException):
    pass


class TokenExpired(AuthException):
    pass


class TokenInvalid(AuthException):
    pass


class LoginNotExists(AuthException):
    pass


class PasswordMismatch(AuthException):
    pass
