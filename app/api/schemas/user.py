from pydantic import BaseModel, field_validator, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def password_length(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value


class UserRegistration(UserBase):
    name: str


