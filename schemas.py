from pydantic import BaseModel, EmailStr
from typing import Optional

# ----------- USER -----------

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


# ----------- PRODUTO -----------

class Produto(BaseModel):
    nome: str
    preco: float
    estoque: int
    categoria: Optional[str] = None