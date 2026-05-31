# routers/ordem_servico_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services.auth_service import get_usuario_atual
from schemas.ordem_servico_schemas import (
    OrdemServicoCreate,
    AtribuirTecnico,
    AlterarStatus,
    OrdemServicoResponse,
)
import services.ordem_servico_service as svc

router = APIRouter(prefix="/ordens-servico", tags=["Ordens de Serviço"])


@router.post("/", response_model=OrdemServicoResponse)
def abrir(
    dados: OrdemServicoCreate,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.abrir_ordem(dados, db)


@router.get("/", response_model=List[OrdemServicoResponse])
def listar(
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.listar_ordens(db)


@router.get("/{os_id}", response_model=OrdemServicoResponse)
def buscar(
    os_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.buscar_ordem(os_id, db)


@router.patch("/{os_id}/atribuir", response_model=OrdemServicoResponse)
def atribuir(
    os_id: int,
    dados: AtribuirTecnico,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.atribuir_tecnico(os_id, dados.tecnico_id, db)


@router.patch("/{os_id}/status", response_model=OrdemServicoResponse)
def alterar_status(
    os_id: int,
    dados: AlterarStatus,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    return svc.alterar_status(os_id, dados.status, dados.observacao, dados.motivo, db)