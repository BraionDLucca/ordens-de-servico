from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class HistoricoStatus(Base):
    __tablename__ = "historico_status"
    id = Column(Integer, primary_key=True, index=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    status_antigo = Column(String, nullable=True) # nulo na abertura
    status_novo = Column(String, nullable=False)
    observacao = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.utcnow)

    ordem = relationship("OrdemServico", back_populates="historicos")