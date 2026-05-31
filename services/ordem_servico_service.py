import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.ordem_servico_model import OrdemServico, StatusOS, PrioridadeOS
import repositories.ordem_servico_repository as repo

# ---------- helpers ----------
def _gerar_numero_os() -> str:
    return "OS-" + str(uuid.uuid4())[:8].upper()

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
    repo.salvar_ordem(os, db)

    os_id: int = os.id  # type: ignore[assignment]
    repo.registrar_historico(db, os_id, None, StatusOS.ABERTA.value, "OS aberta")

    return repo.commit_e_refresh(os, db)

# ---------- listar ----------
def listar_ordens(db: Session):
    return repo.listar_todos(db)

def buscar_ordem(os_id: int, db: Session) -> OrdemServico:
    os = repo.buscar_por_id(os_id, db)
    if os is None:
        raise HTTPException(404, "Ordem de serviço não encontrada")
    return os

# ---------- atribuir técnico ----------
def atribuir_tecnico(os_id: int, tecnico_id: int, db: Session) -> OrdemServico:
    os = buscar_ordem(os_id, db)

    status_atual: str = os.status.value  # type: ignore[union-attr]
    if status_atual == StatusOS.CONCLUIDA.value:
        raise HTTPException(400, "OS concluída não pode ser alterada")

    if repo.contar_em_andamento_por_tecnico(tecnico_id, db) >= 5:
        raise HTTPException(400, "Técnico já possui 5 OS em andamento")

    repo.atualizar_ordem(os_id, {"tecnico_id": tecnico_id, "status": StatusOS.EM_ANDAMENTO}, db)
    repo.registrar_historico(
        db, os_id,
        status_atual,
        StatusOS.EM_ANDAMENTO.value,
        f"Técnico {tecnico_id} atribuído",
    )
    return repo.commit_e_refresh(os, db)

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
        if os.tecnico_id is None:  # type: ignore[union-attr]
            raise HTTPException(400, "OS não pode ser concluída sem técnico responsável")
        updates["data_conclusao"] = datetime.utcnow()

    if novo_status == StatusOS.CANCELADA:
        if not motivo:
            raise HTTPException(400, "Motivo obrigatório para cancelamento")
        updates["motivo_cancelamento"] = motivo

    repo.atualizar_ordem(os_id, updates, db)
    repo.registrar_historico(db, os_id, status_atual, novo_status.value, observacao)
    return repo.commit_e_refresh(os, db)