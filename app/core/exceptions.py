class AppException(Exception):
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
        
class UserNotFoundError(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            message=f"User with ID '{user_id}' not found",
            status_code=404
        )
        
class MaterialAlreadyExistsError(AppException):
    def __init__(self, sku: str):
        super().__init__(
            message=f"Material with SKU '{sku}' already exists",
            status_code=409
        )
        
class MaterialNotFoundError(AppException):
    def __init__(self, material_id: int):
        super().__init__(
            message=f"Material with ID '{material_id}' not found",
            status_code=404
        )
        
class InsufficientInventoryError(AppException):
    def __init__(self, material_id: int, available_quantity: float, requested_quantity: float):
        super().__init__(
            message=f"Insufficient inventory for material ID '{material_id}'. Only have {available_quantity}, but {requested_quantity} was requested.",
            status_code=400
        )
        
class LockInventoryError(AppException):
    def __init__(self, material_id: int):
        super().__init__(
            message=f"Please try again later.The element with '{material_id}' is being updated by another process.",
            status_code=500
        )
        
class MaterialWithActiveInventoryError(AppException):
    def __init__(self, material_id: int, available_quantity: float):
        super().__init__(
            message=f"Cannot delete material ID '{material_id}' because it has active inventory of {available_quantity}.",
            status_code=400
        )