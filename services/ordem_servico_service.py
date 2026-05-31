# services/ordem_servico_service.py
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.ordem_servico_model import OrdemServico, StatusOS, PrioridadeOS
from models.historico_status_model import HistoricoStatus


# ---------- helpers ----------
def _gerar_numero_os() -> str:
    return "OS-" + str(uuid.uuid4())[:8].upper()


def _registrar_historico(
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


# ---------- abrir OS ----------
def abrir_ordem(dados, db: Session) -> OrdemServico:
    prioridade = PrioridadeOS[dados.prioridade]
    os = OrdemServico(
        numero_os=_gerar_numero_os(),
        cliente_id=dados.cliente_id,
        equipamento=dados.equipamento,
        descricao_problema=dados.descricao_problema,
        prioridade=prioridade,
        status=StatusOS.ABERTA,
        data_abertura=datetime.utcnow(),
    )
    db.add(os)
    db.flush()

    os_id: int = os.id  # type: ignore[assignment]
    _registrar_historico(db, os_id, None, StatusOS.ABERTA.value, "OS aberta")
    db.commit()
    db.refresh(os)
    return os


# ---------- listar ----------
def listar_ordens(db: Session):
    return db.query(OrdemServico).all()


def buscar_ordem(os_id: int, db: Session) -> OrdemServico:
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if os is None:
        raise HTTPException(404, "Ordem de serviço não encontrada")
    return os


# ---------- atribuir técnico ----------
def atribuir_tecnico(os_id: int, tecnico_id: int, db: Session) -> OrdemServico:
    os = buscar_ordem(os_id, db)

    status_atual: str = os.status.value  # type: ignore[union-attr]
    if status_atual == StatusOS.CONCLUIDA.value:
        raise HTTPException(400, "OS concluída não pode ser alterada")

    em_andamento = db.query(OrdemServico).filter(
        OrdemServico.tecnico_id == tecnico_id,
        OrdemServico.status == StatusOS.EM_ANDAMENTO,
    ).count()

    if em_andamento >= 5:
        raise HTTPException(400, "Técnico já possui 5 OS em andamento")

    db.query(OrdemServico).filter(OrdemServico.id == os_id).update(
        {"tecnico_id": tecnico_id, "status": StatusOS.EM_ANDAMENTO}
    )
    _registrar_historico(
        db, os_id,
        status_atual,
        StatusOS.EM_ANDAMENTO.value,
        f"Técnico {tecnico_id} atribuído",
    )
    db.commit()
    db.refresh(os)
    return os


# ---------- alterar status ----------
def alterar_status(
    os_id: int,
    novo_status_str: str,
    observacao: Optional[str] = None,
    motivo: Optional[str] = None,
    db: Session = None,  # type: ignore[assignment]
) -> OrdemServico:
    os = buscar_ordem(os_id, db)

    status_atual: str = os.status.value  # type: ignore[union-attr]
    if status_atual == StatusOS.CONCLUIDA.value:
        raise HTTPException(400, "OS concluída não pode ser alterada")

    novo_status = StatusOS[novo_status_str]
    updates: dict = {"status": novo_status}

    if novo_status == StatusOS.CONCLUIDA:
        tecnico_id = os.tecnico_id  # type: ignore[union-attr]
        if tecnico_id is None:
            raise HTTPException(400, "OS não pode ser concluída sem técnico responsável")
        updates["data_conclusao"] = datetime.utcnow()

    if novo_status == StatusOS.CANCELADA:
        if not motivo:
            raise HTTPException(400, "Motivo obrigatório para cancelamento")
        updates["motivo_cancelamento"] = motivo

    db.query(OrdemServico).filter(OrdemServico.id == os_id).update(updates)
    _registrar_historico(db, os_id, status_atual, novo_status.value, observacao)
    db.commit()
    db.refresh(os)
    return os