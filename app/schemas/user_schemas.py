from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str
    role : str | None
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "name": "John Doe",
                "email": "john@gmail.com",
                "password": "strongpassword123",
                "role": "operator"
            }
        }
    )

class UserRead(BaseModel):
    id : int
    name : str
    email : EmailStr
    role : str
    is_active : bool
    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "name": "John Doe",
                "email": "jonh@gmail.com",
                "role": "operator",
                "is_active": True
            }
        }
    )

class TokenResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"

class UserUpdate(BaseModel):
    name : str | None
    email : EmailStr | None
    role : str | None
    is_active : bool | None
    password : str | None
    model_config = ConfigDict(from_attributes = True)
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str