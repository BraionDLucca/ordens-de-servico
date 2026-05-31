from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrdemServicoCreate(BaseModel):
    cliente_id: int
    equipamento: str
    descricao_problema: str
    prioridade: str = "MEDIA" # BAIXA | MEDIA | ALTA | URGENTE

class AtribuirTecnico(BaseModel):
    tecnico_id: int

class AlterarStatus(BaseModel):
    status: str # ABERTA | EM_ANDAMENTO | AGUARDANDO_PECA | CONCLUIDA | CANCELADA
    observacao: Optional[str] = None
    motivo: Optional[str] = None # obrigatório se status=CANCELADA

class OrdemServicoResponse(BaseModel):
    id: int
    numero_os: str
    cliente_id: int
    tecnico_id: Optional[int]
    equipamento: str
    descricao_problema: str
    status: str
    prioridade: str
    data_abertura: datetime
    data_conclusao: Optional[datetime]
    
    class Config:
        from_attributes = True