from database import SessionLocal, engine
from fastapi import FastAPI
from auth import hash_senha, verificar_senha, criar_token
from models import Usuario, UsuarioModel, Produto, ProdutoModel, Carrinho, CarrinhoModel, Pedido, PedidoModel

app = FastAPI()

@app.post("/register")
def registrar(usuario: Usuario):
    db = SessionLocal()
    db_usuario = UsuarioModel(email=usuario.email, senha_hash=hash_senha(usuario.senha))
    db.add(db_usuario)
    db.commit()
    db.close()
    return usuario

@app.post("/login")
def login(usuario: Usuario):
    db = SessionLocal()
    db_usuario = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if not verificar_senha(usuario.senha, db_usuario.senha_hash):
        return {"erro": "Senha incorreta"}
    token = criar_token({"sub": usuario.email})
    return {"access_token": token}

@app.get("/produtos")
def listar_produtos():
    db = SessionLocal()
    produtos = db.query(ProdutoModel).all()
    db.close()
    return produtos

@app.post("/produtos")
def criar_produto(produto: Produto):
    db = SessionLocal()
    db_produto = ProdutoModel(
        nome=produto.nome,
        preco=produto.preco,
        estoque=produto.estoque,
        categoria=produto.categoria,
    )
    db.add(db_produto)
    db.commit()
    db.close()
    return {
        "nome": produto.nome,
        "preco": produto.preco,
        "estoque": produto.estoque,
        "categoria": produto.categoria,
    }

@app.get("/carrinhos")
def listar_carrinhos():
    db = SessionLocal()
    carrinhos = db.query(CarrinhoModel).all()
    db.close()
    return carrinhos

@app.post("/carrinhos")
def criar_carrinho(carrinho: Carrinho):
    db = SessionLocal()
    db_carrinho = CarrinhoModel(
        usuario_id=carrinho.usuario_id,
        produto_id=carrinho.produto_id,
    )
    db.add(db_carrinho)
    db.commit()
    db.close()
    return {
        "usuario_id": carrinho.usuario_id,
        "produto_id": carrinho.produto_id,
    }

@app.delete("/carrinhos/{carinho_id}")
def delete_carrinho(carrinho_id: int):
    db = SessionLocal()
    carrinho =db.query(CarrinhoModel).filter(CarrinhoModel.id == carrinho_id).first()
    db.delete(carrinho)
    db.commit()
    db.close()
    return carrinho

@app.get("/pedidos")
def listar_pedidos():
    db = SessionLocal()
    pedidos = db.query(PedidoModel).all()
    db.close()
    return pedidos

@app.post("/pedidos")
def criar_pedido(pedido: Pedido):
    db = SessionLocal()
    db_pedido = PedidoModel(
        usuario_id=pedido.usuario_id,
        total=pedido.total,
        status=pedido.status
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    db.close()
    return {
        "id": db_pedido.id,
        "usuario_id": db_pedido.usuario_id,
        "total": db_pedido.total,
        "status": db_pedido.status
    }