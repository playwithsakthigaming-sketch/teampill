from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    username: str = Field(min_length=3,max_length=30)

    email: EmailStr

    password: str = Field(min_length=8)


class LoginSchema(BaseModel):
    email: EmailStr

    password: str


class TokenResponse(BaseModel):
    access_token: str

    refresh_token: str

    token_type: str = "Bearer"
