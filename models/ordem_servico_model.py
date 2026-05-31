from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

class StatusOS(enum.Enum):
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    AGUARDANDO_PECA = "AGUARDANDO_PECA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

class PrioridadeOS(enum.Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"

class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True, index=True)
    numero_os = Column(String, unique=True, index=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    equipamento = Column(String, nullable=False)
    descricao_problema = Column(String, nullable=False)
    status = Column(Enum(StatusOS), default=StatusOS.ABERTA, nullable=False)
    prioridade = Column(Enum(PrioridadeOS), default=PrioridadeOS.MEDIA, nullable=False)
    data_abertura = Column(DateTime, default=datetime.utcnow)
    data_conclusao = Column(DateTime, nullable=True)
    motivo_cancelamento = Column(String, nullable=True)

    cliente = relationship("Cliente", back_populates="ordens")
    tecnico = relationship("Usuario")
    historicos = relationship("HistoricoStatus", back_populates="ordem", cascade="all, delete-orphan")