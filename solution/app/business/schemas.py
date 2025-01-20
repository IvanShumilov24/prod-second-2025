from pydantic import BaseModel, EmailStr

class BusinessCreate(BaseModel):
    name: str
    email: EmailStr
    password: str # iamthewinner!!!!
