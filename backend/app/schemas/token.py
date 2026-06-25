from pydantic import BaseModel


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"


class RefreshSchema(BaseModel):

    refresh_token: str
