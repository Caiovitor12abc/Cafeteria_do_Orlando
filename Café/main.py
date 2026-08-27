from fastapi import FastAPI

app = FastAPI(title="API da Cafetaria")

@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API da Cafetaria! ☕"}

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db

# Cria automaticamente a tabela se ela não existir
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API da Cafetaria ☕")

@app.post("/api/produtos", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    # Converte o schema para o modelo de BD
    novo_produto = models.ProdutoBD(**produto.model_dump())
    
    db.add(novo_produto)
    db.commit() # Grava no ficheiro SQLite
    db.refresh(novo_produto) # Recupera o ID gerado
    
    return novo_produto
from fastapi import HTTPException
from typing import List

# Listar todos os produtos
@app.get("/api/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.ProdutoBD).all()

# Buscar produto por ID
@app.get("/api/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.ProdutoBD).filter(models.ProdutoBD.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado na cafetaria"
        )
    return produto

    # Atualizar Produto
@app.put("/api/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados_novos: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    query = db.query(models.ProdutoBD).filter(models.ProdutoBD.id == produto_id)
    produto = query.first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    query.update(dados_novos.model_dump(), synchronize_session=False)
    db.commit()
    
    return query.first()

# Remover Produto
@app.delete("/api/produtos/{produto_id}")
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.ProdutoBD).filter(models.ProdutoBD.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    
    return {"mensagem": f"Produto '{produto.nome}' removido com sucesso"}

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Completa - Cafetaria Backend ☕")

# Configuração de CORS para autorizar qualquer Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTAS ---

@app.post("/api/produtos", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = models.ProdutoBD(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.get("/api/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.ProdutoBD).all()

@app.get("/api/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.ProdutoBD).filter(models.ProdutoBD.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/api/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados_novos: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    query = db.query(models.ProdutoBD).filter(models.ProdutoBD.id == produto_id)
    if not query.first():
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    query.update(dados_novos.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()

@app.delete("/api/produtos/{produto_id}")
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.ProdutoBD).filter(models.ProdutoBD.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(produto)
    db.commit()
    return {"mensagem": f"Produto ID {produto_id} removido com sucesso"}