from pydantic import EmailStr, BaseModel


class LoginInput(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
