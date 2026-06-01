from pydantic import BaseModel
from typing import Optional

class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    quantidade_estoque: int = 0
    preco: float

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    quantidade_estoque: int
    preco: float

    class Config:
        from_attributes = True