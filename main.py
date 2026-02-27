from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import UserCreate, UserLogin, UserResponse
from models import (
    Base,
    Usuario,
    UsuarioModel,
    Produto,
    ProdutoModel,
    Carrinho,
    CarrinhoModel,
    Pedido,
    PedidoModel
)
from auth import hash_senha, verificar_senha, criar_token, verificar_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ----------------- Dependência de DB -----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- Auth -----------------

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserResponse
from auth import hash_senha


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Verifica se email já existe
    usuario_existente = db.query(User).filter(User.email == user.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Cria novo usuário
    novo_usuario = User(
        email=user.email,
        senha=hash_senha(user.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

from schemas import UserLogin
from auth import verificar_senha, criar_token


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    usuario = db.query(User).filter(User.email == user.email).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not verificar_senha(user.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}

# ----------------- Produtos -----------------

@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoModel).all()

@app.post("/produtos")
def criar_produto(
    produto: Produto,
    db: Session = Depends(get_db),
    user=Depends(verificar_token)
):
    db_produto = ProdutoModel(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# ----------------- Carrinho -----------------

@app.delete("/carrinhos/{carrinho_id}")
def delete_carrinho(
    carrinho_id: int,
    db: Session = Depends(get_db),
    user=Depends(verificar_token)
):
    carrinho = db.query(CarrinhoModel).filter(CarrinhoModel.id == carrinho_id).first()

    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    db.delete(carrinho)
    db.commit()
    return {"mensagem": "Carrinho removido"}