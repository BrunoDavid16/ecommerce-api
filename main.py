from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
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

@app.post("/register")
def registrar(usuario: Usuario, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_usuario = UsuarioModel(
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    return {"mensagem": "Usuário criado com sucesso"}

@app.post("/login")
def login(usuario: Usuario, db: Session = Depends(get_db)):
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()

    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verificar_senha(usuario.senha, db_usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    token = criar_token({"sub": usuario.email})
    return {"access_token": token}

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