from typing import Optional
from sqlalchemy.orm import Session
from models.ordem_servico_model import OrdemServico, StatusOS
from models.historico_status_model import HistoricoStatus

# Persiste a OS e faz flush para gerar o ID (sem commit).
def salvar_ordem(os: OrdemServico, db: Session) -> OrdemServico:
    db.add(os)
    db.flush()
    return os

def listar_todos(db: Session):
    return db.query(OrdemServico).all()

def buscar_por_id(os_id: int, db: Session):
    return db.query(OrdemServico).filter(OrdemServico.id == os_id).first()

def contar_em_andamento_por_tecnico(tecnico_id: int, db: Session) -> int:
    return (
        db.query(OrdemServico)
        .filter(
            OrdemServico.tecnico_id == tecnico_id,
            OrdemServico.status == StatusOS.EM_ANDAMENTO,
        )
        .count()
    )

def atualizar_ordem(os_id: int, updates: dict, db: Session) -> None:
    db.query(OrdemServico).filter(OrdemServico.id == os_id).update(updates)

def registrar_historico(
    db: Session,
    ordem_id: int,
    status_antigo: Optional[str],
    status_novo: str,
    observacao: Optional[str] = None,
) -> None:
    h = HistoricoStatus(
        ordem_servico_id=ordem_id,
        status_antigo=status_antigo,
        status_novo=status_novo,
        observacao=observacao,
    )
    db.add(h)

def commit_e_refresh(os: OrdemServico, db: Session) -> OrdemServico:
    db.commit()
    db.refresh(os)
    return os