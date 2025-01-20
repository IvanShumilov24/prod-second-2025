import re

from pydantic import BaseModel, Field, field_validator


class UserTargetSettings(BaseModel):
    age: int = Field(max_length=100, min_length=0)
    country: str

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    surname: str = Field(min_length=1, max_length=120)
    email: str = Field(max_length=120, min_length=8)
    avatar_url: str = Field(max_length=350)
    other: UserTargetSettings

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    surname: str = Field(min_length=1, max_length=120)
    avatar_url: str = Field(max_length=350)

class UserCreate(UserBase):
    email: str = Field(max_length=120, min_length=8)
    password: str = Field(min_length=8, max_length=60)
    other: UserTargetSettings

    @field_validator("password")
    def validate_password(cls, password):
        if not re.fullmatch(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                password
        ):
            raise ValueError(
                "Пароль должен содержать латинские буквы, хотя бы одну заглавную, одну строчную, "
                "одну цифру и специальные символы, и быть не менее 8 символов."
            )
        return password

class UserUpdate(UserBase):
    password: str = Field(min_length=8, max_length=60)