from typing import Optional
from sqlalchemy.orm import Session
from models.cliente_model import Cliente

def buscar_por_cpf(cpf: str, db: Session):
    return db.query(Cliente).filter(Cliente.cpf == cpf).first()

def buscar_por_id(cliente_id: int, db: Session):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def listar_todos(db: Session):
    return db.query(Cliente).all()

def buscar_filtros(
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

# Persiste um novo cliente (add + commit + refresh).
def salvar(cliente: Cliente, db: Session) -> Cliente:
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

# Confirma alterações em um cliente já rastreado pela sessão.
def salvar_alteracoes(cliente: Cliente, db: Session) -> Cliente:
    db.commit()
    db.refresh(cliente)
    return cliente

def deletar(cliente: Cliente, db: Session) -> None:
    db.delete(cliente)
    db.commit()
