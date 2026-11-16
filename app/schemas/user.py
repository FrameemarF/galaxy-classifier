from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from app.models.user import UserRole

class Register(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"