# routers/cliente_router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from services.auth_service import get_usuario_atual
from schemas.cliente_schemas import ClienteCreate, ClienteUpdate, ClienteResponse
import services.cliente_service as svc

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse)
def criar(
    dados: ClienteCreate,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.criar_cliente(dados, db)


@router.get("/", response_model=List[ClienteResponse])
def listar(
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.listar_clientes(db)


@router.get("/busca", response_model=List[ClienteResponse])
def buscar(
    nome: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    telefone: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.buscar_clientes(nome, email, telefone, cpf, db)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def editar(
    cliente_id: int,
    dados: ClienteUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.editar_cliente(cliente_id, dados, db)


@router.delete("/{cliente_id}")
def deletar(
    cliente_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.deletar_cliente(cliente_id, db)