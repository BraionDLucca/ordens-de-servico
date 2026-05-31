from pydantic import BaseModel
from typing import Optional

class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    # endereco NÃO vem do usuário — é preenchido pelo ViaCEP

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None

class ClienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    telefone: Optional[str]
    email: Optional[str]
    endereco: Optional[str]
    
    class Config:
        from_attributes = True