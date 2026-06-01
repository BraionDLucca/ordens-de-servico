from sqlalchemy.orm import Session
from models.produto_model import Peca

def buscar_por_id(produto_id: int, db: Session):
    return db.query(Peca).filter(Peca.id == produto_id).first()

def listar_todos(db: Session):
    return db.query(Peca).all()

def salvar(produto: Peca, db: Session) -> Peca:
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto