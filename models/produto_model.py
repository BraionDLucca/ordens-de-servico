from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base

class TipoMovimentacao(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Peca(Base):
    __tablename__ = "pecas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=True)
    quantidade_estoque = Column(Integer, default=0, nullable=False)
    preco = Column(Float, nullable=False)

    historicos = relationship("HistoricoPeca", back_populates="peca", cascade="all, delete-orphan")
    uso_os = relationship("PecaOrdemServico", back_populates="peca", cascade="all, delete-orphan")



