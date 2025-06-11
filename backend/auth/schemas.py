from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    subscription: str | None = "free"


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
