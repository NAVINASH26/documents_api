
from pydantic import BaseModel, EmailStr,field_validator

allowed_emails=["gmail.com", "yahoo.com", "outlook.com"]

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email')
    @classmethod
    def validate_domian(cls,value):
        domain=value.split("@")[1]

        if domain not in allowed_emails:
            raise ValueError("only gmail,yahoo and outlook are allowed")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str