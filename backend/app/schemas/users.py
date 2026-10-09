from datetime import datetime
from pydantic import BaseModel , ConfigDict , EmailStr
from app.database.models.user import UserRole


class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    role : UserRole = UserRole.CASHIER


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    username:str
    email:EmailStr
    role:UserRole
    is_active:bool
    created_at:datetime

    