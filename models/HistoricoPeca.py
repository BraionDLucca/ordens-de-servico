from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base
from models.produto_model import TipoMovimentacao

class HistoricoPeca(Base):
    """
    Tabela de auditoria: toda movimentação (entrada por compra ou saída por uso em OS) fica registrada aqui.
    """
    __tablename__ = "historico_pecas"

    id = Column(Integer, primary_key=True, index=True)
    peca_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)
    ordem_servico_id = Column(Integer, nullable=True) # Pode ser nulo se a entrada for só um ajuste de estoque
    tipo = Column(Enum(TipoMovimentacao), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    motivo = Column(String, nullable=True) # Ex: "Compra de lote", "Uso na OS #123"

    peca = relationship("Peca", back_populates="historicos")