# E-commerce API

API RESTful para gerenciamento de usuários, produtos e pedidos com autenticação JWT.

## 🚀 Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)

---

## 🔐 Funcionalidades

- Cadastro de usuário
- Login com geração de token JWT
- Hash seguro de senha com bcrypt
- Proteção de rotas com autenticação
- CRUD de produtos
- Gerenciamento de carrinho
- Criação de pedidos

---

## 🌐 API ao vivo
Acesse a documentação em: https://ecommerce-api-3nrs.onrender.com/docs

---

## 🛠 Como executar localmente

Clone o repositório:
```bash
git clone https://github.com/BrunoDavid16/ecommerce-api.git
cd ecommerce-api
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Rode a API:
```bash
python -m uvicorn main:app --reload
```

Acesse a documentação em:
```
http://127.0.0.1:8000/docs
```

---

## 📦 Rotas

### Autenticação
- **POST** `/register` — cria um novo usuário
- **POST** `/login` — autentica e retorna o token JWT

### Produtos
- **GET** `/produtos` — lista todos os produtos
- **POST** `/produtos` — cria um produto

### Carrinho
- **GET** `/carrinhos` — lista itens do carrinho
- **POST** `/carrinhos` — adiciona item ao carrinho
- **DELETE** `/carrinhos/{carrinho_id}` — remove item do carrinho

### Pedidos
- **GET** `/pedidos` — lista todos os pedidos
- **POST** `/pedidos` — cria um pedido