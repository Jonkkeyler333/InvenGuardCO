class AppException(Exception):
    """Base exception for the application"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserAlreadyExistsError(AppException):
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists",
            status_code=409
        )

class UserNotFoundError(AppException):
    def __init__(self, identifier: str | int):
        super().__init__(
            message=f"User '{identifier}' not found",
            status_code=404
        )

class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            status_code=401
        )

class InvalidTokenError(AppException):
    def __init__(self, reason: str = "Invalid or expired token"):
        super().__init__(
            message=reason,
            status_code=401
        )

class UnauthorizedError(AppException):
    def __init__(self, message: str = "Not authorized to perform this action"):
        super().__init__(
            message=message,
            status_code=403
        )