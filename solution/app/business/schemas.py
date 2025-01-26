import re

from pydantic import BaseModel, EmailStr, UUID4, Field, field_validator


class Business(BaseModel):
    id: UUID4
    name: str = Field(min_length=5, max_length=50)
    email: EmailStr
    password: str  # iamthewinner!!!!


class BusinessBase(BaseModel):
    name: str = Field(min_length=5, max_length=50)
    email: EmailStr


class BusinessCreate(BusinessBase):
    password: str




class BusinessUpdate(BaseModel):
    password: str


class BusinessCreateDB(BusinessBase):
    hashed_password: str


class BusinessUpdateDB(BaseModel):
    hashed_password: str


class BusinessAuthResponse(BaseModel):
    token: str
    company_id: UUID4

class Auth(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password", check_fields=False)
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