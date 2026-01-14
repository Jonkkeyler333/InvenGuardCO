class AppException(Exception):
    """Base exception for the application"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid credentials",
            status_code=401
        )
        
class UnauthorizedError(AppException):
    def __init__(self, message: str = "Not authorized to perform this action"):
        super().__init__(
            message=message,
            status_code=403
        )

class UserAlreadyExistsError(AppException):
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists",
            status_code=409
        )