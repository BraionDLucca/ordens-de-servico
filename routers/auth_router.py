# routers/auth_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth_schemas import LoginRequest, TokenResponse, UsuarioCreate, UsuarioResponse
from services.auth_service import login, criar_usuario, get_usuario_atual
from models.usuario_model import PerfilUsuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResponse)
def fazer_login(dados: LoginRequest, db: Session = Depends(get_db)):
    return login(dados.email, dados.senha, db)

@router.post("/usuarios", response_model=UsuarioResponse)
def registrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    perfil = PerfilUsuario[dados.perfil]
    return criar_usuario(dados.nome, dados.email, dados.senha, perfil, db)

@router.get("/me", response_model=UsuarioResponse)
def meu_perfil(usuario_atual=Depends(get_usuario_atual)):
    return usuario_atual