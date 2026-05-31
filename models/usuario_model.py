# models/usuario_model.py
from sqlalchemy import Column, Integer, String, Enum
from core.database import Base
import enum

class PerfilUsuario(enum.Enum):
    ADMIN    = "ADMIN"
    TECNICO  = "TECNICO"
    ATENDENTE = "ATENDENTE"

class Usuario(Base):
    __tablename__ = "usuarios"
    id         = Column(Integer, primary_key=True, index=True)
    nome       = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    perfil     = Column(Enum(PerfilUsuario), nullable=False)