import json
import urllib.request
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.cliente_model import Cliente
import repositories.cliente_repository as repo

# ---------- ViaCEP ----------
def buscar_endereco_cep(cep: str) -> Optional[str]:
    cep_limpo = cep.replace("-", "").strip()
    try:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        with urllib.request.urlopen(url, timeout=5) as resp:
            dados = json.loads(resp.read().decode())
        if "erro" in dados:
            return None
        return (
            f"{dados.get('logradouro', '')}, "
            f"{dados.get('bairro', '')}, "
            f"{dados.get('localidade', '')} - "
            f"{dados.get('uf', '')}"
        )
    except Exception:
        return None

# ---------- CRUD ----------
def criar_cliente(dados, db: Session) -> Cliente:
    if repo.buscar_por_cpf(dados.cpf, db):
        raise HTTPException(400, "CPF já cadastrado")

    endereco: Optional[str] = buscar_endereco_cep(dados.cep) if dados.cep else None

    cliente = Cliente(
        nome=dados.nome,
        cpf=dados.cpf,
        telefone=dados.telefone,
        email=dados.email,
        cep=dados.cep,
        endereco=endereco,
    )
    return repo.salvar(cliente, db)

def listar_clientes(db: Session):
    return repo.listar_todos(db)

def buscar_clientes(
    nome: Optional[str],
    email: Optional[str],
    telefone: Optional[str],
    cpf: Optional[str],
    db: Session,
) -> list:
    return repo.buscar_filtros(nome, email, telefone, cpf, db)

def editar_cliente(cliente_id: int, dados, db: Session) -> Cliente:
    cliente = repo.buscar_por_id(cliente_id, db)
    if cliente is None:
        raise HTTPException(404, "Cliente não encontrado")

    if dados.nome is not None:
        cliente.nome = dados.nome                          # type: ignore[assignment]
    if dados.telefone is not None:
        cliente.telefone = dados.telefone                  # type: ignore[assignment]
    if dados.email is not None:
        cliente.email = dados.email                        # type: ignore[assignment]
    if dados.cep is not None:
        cliente.cep = dados.cep                            # type: ignore[assignment]
        cliente.endereco = buscar_endereco_cep(dados.cep)  # type: ignore[assignment]

    return repo.salvar_alteracoes(cliente, db)

def deletar_cliente(cliente_id: int, db: Session):
    cliente = repo.buscar_por_id(cliente_id, db)
    if cliente is None:
        raise HTTPException(404, "Cliente não encontrado")
    repo.deletar(cliente, db)
    return {"ok": True}