from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import Optional

class Base(DeclarativeBase):
    pass

class Usuario(BaseModel):
    email: str
    senha: str

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    senha_hash = Column(String)

class Produto(BaseModel):
    nome: str
    preco: float
    estoque: int
    categoria: Optional[str]

class ProdutoModel(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    preco = Column(Float)
    estoque = Column(Integer)
    categoria = Column(String)

class Carrinho(BaseModel):
    usuario_id: int
    produto_id: int

class CarrinhoModel(Base):
    __tablename__ = "carrinhos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))

class Pedido(BaseModel):
    usuario_id: int
    total: float
    status: str

class PedidoModel(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    total = Column(Float)
    status = Column(String)