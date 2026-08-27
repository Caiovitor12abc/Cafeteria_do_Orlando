from pydantic import BaseModel
from typing import Optional

# Dados para CRIAR ou ATUALIZAR
class ProdutoCreate(BaseModel):
    nome: str
    categoria: str
    preco: float
    disponivel: Optional[bool] = True

# Dados RETORNADOS (incluem o ID gerado pelo banco)
class ProdutoResponse(ProdutoCreate):
    id: int

    class Config:
        from_attributes = True