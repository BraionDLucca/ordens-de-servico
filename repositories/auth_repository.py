from sqlalchemy.orm import Session
from models.usuario_model import Usuario

def buscar_por_email(email: str, db: Session):
    return db.query(Usuario).filter(Usuario.email == email).first()

def buscar_por_id(user_id: int, db: Session):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def salvar_usuario(usuario: Usuario, db: Session) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario