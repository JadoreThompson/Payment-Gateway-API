from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


# Auth Models
class User(BaseModel):
    email: EmailStr
    password: Optional[str]

    @field_validator('password')
    @classmethod
    def check_password(cls, password: str):
        min_nums = 2
        min_length = 8
        if len(password) <= min_length:
            raise ValueError("Password must have minimum 8 characters")
        if sum(1 for char in password if char.isdigit()) < min_nums:
            raise ValueError(f"Password must have minimum {min_nums} characters")
        return password


class SignUpBody(User):
    fname: str
