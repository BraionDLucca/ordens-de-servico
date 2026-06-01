from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from core.database import Base


class PecaOrdemServico(Base):
  
    __tablename__ = "peca_ordem_servico"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
    ordem_servico_id = Column(Integer, index=True, nullable=False) 
    peca_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False) 
=======
    ordem_servico_id = Column(Integer, index=True, nullable=False) # ID gerado pelo módulo de OS do seu colega
    peca_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False) # Registra o preço no momento do uso
>>>>>>> origin/main

    peca = relationship("Peca", back_populates="uso_os")