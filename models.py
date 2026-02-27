from sqlalchemy import Column, Integer, String, Float, ForeignKey
from pydantic import BaseModel
from typing import Optional
from database import Base

# ----------------- Pydantic Schemas -----------------

class Usuario(BaseModel):
    email: str
    senha: str

class Produto(BaseModel):
    nome: str
    preco: float
    estoque: int
    categoria: Optional[str] = None

class Carrinho(BaseModel):
    usuario_id: int
    produto_id: int

class Pedido(BaseModel):
    usuario_id: int
    total: float
    status: str

# ----------------- SQLAlchemy Models -----------------

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoria = Column(String)

class CarrinhoModel(Base):
    __tablename__ = "carrinhos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))

class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    total = Column(Float)
    status = Column(String)