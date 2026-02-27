# schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional


# -------- USER --------

class UserCreate(BaseModel):
    email: EmailStr
    senha: str


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# -------- PRODUCT --------

class ProductCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float


class ProductResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float

    class Config:
        from_attributes = True