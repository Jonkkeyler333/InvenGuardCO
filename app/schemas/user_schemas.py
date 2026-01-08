from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    username : str 
    name : str
    email : EmailStr
    password : str
    role : str | None

class UserRead(BaseModel):
    id : int
    username : str 
    name : str
    email : EmailStr
    role : str
    is_active : bool
    model_config = ConfigDict(from_attributes = True)

class UserUpdate(BaseModel):
    name : str | None
    email : EmailStr | None
    role : str | None
    is_active : bool | None
    model_config = ConfigDict(from_attributes = True)
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str