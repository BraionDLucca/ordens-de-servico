from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services.auth_service import get_usuario_atual
from schemas.produto_schemas import ProdutoCreate, ProdutoResponse
import services.produto_service as svc

router = APIRouter(prefix="/produtos", tags=["Produtos de Estoque"])

@router.post("/", response_model=ProdutoResponse)
def criar(
    dados: ProdutoCreate,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual)
):
    return svc.criar_produto(dados, db)

@router.get("/", response_model=List[ProdutoResponse])
def listar(
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual)
):
    return svc.listar_produtos(db)