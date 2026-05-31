from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    cpf = Column(String, unique=True, nullable=False, index=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    cep = Column(String, nullable=True)
    endereco = Column(String, nullable=True) # preenchido automaticamente via ViaCEP
    
    ordens = relationship("OrdemServico", back_populates="cliente")