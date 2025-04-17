# flask_app/exceptions.py
class AuthException(Exception):
    """Base authentication exception"""

    status_code = 400


class ValidationError(AuthException):
    """Raised when input validation fails"""

    pass


class AuthenticationError(AuthException):
    """Raised when authentication fails"""

    status_code = 401


class AccountLockedError(AuthException):
    """Raised when account is temporarily locked"""

    status_code = 403


class EmailNotVerifiedError(AuthException):
    """Raised when email is not verified"""

    status_code = 403


class TokenExpiredError(AuthException):
    """Raised when token has expired"""

    status_code = 400


class TokenInvalidError(AuthException):
    """Raised when token is invalid"""

    status_code = 400


class EmailAlreadyVerifiedError(AuthException):
    """Raised when email is already verified"""

    status_code = 400


class TooManyRequestsError(AuthException):
    """Raised when too many requests are made"""

    status_code = 429


class UserNotFoundError(AuthException):
    """Raised when user is not found"""

    status_code = 404
