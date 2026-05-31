# services/cliente_service.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.cliente_model import Cliente


# ---------- ViaCEP ----------
def buscar_endereco_cep(cep: str) -> Optional[str]:
    cep_limpo = cep.replace("-", "").strip()
    try:
        import urllib.request
        import json
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
    existente = db.query(Cliente).filter(Cliente.cpf == dados.cpf).first()
    if existente:
        raise HTTPException(400, "CPF já cadastrado")

    endereco: Optional[str] = None
    if dados.cep:
        endereco = buscar_endereco_cep(dados.cep)

    cliente = Cliente(
        nome=dados.nome,
        cpf=dados.cpf,
        telefone=dados.telefone,
        email=dados.email,
        cep=dados.cep,
        endereco=endereco,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar_clientes(db: Session):
    return db.query(Cliente).all()


def buscar_clientes(
    nome: Optional[str],
    email: Optional[str],
    telefone: Optional[str],
    cpf: Optional[str],
    db: Session,
) -> list:
    q = db.query(Cliente)
    if nome:
        q = q.filter(Cliente.nome.ilike(f"%{nome}%"))
    if email:
        q = q.filter(Cliente.email.ilike(f"%{email}%"))
    if telefone:
        q = q.filter(Cliente.telefone.contains(telefone))
    if cpf:
        q = q.filter(Cliente.cpf.contains(cpf))
    return q.all()


def editar_cliente(cliente_id: int, dados, db: Session) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
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

    db.commit()
    db.refresh(cliente)
    return cliente


def deletar_cliente(cliente_id: int, db: Session):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(404, "Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"ok": True}