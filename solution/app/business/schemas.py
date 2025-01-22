from pydantic import BaseModel, EmailStr, UUID4, Field


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
