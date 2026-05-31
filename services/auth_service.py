import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from core.database import get_db
from models.usuario_model import Usuario, PerfilUsuario
import repositories.auth_repository as repo

SECRET_KEY = "segredo"
ALGORITHM = "HS256"
EXPIRE_MIN = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha_plana.encode("utf-8"), senha_hash.encode("utf-8"))

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def login(email: str, senha: str, db: Session) -> dict:
    usuario = repo.buscar_por_email(email, db)
    if usuario is None or not verificar_senha(senha, str(usuario.senha_hash)):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil.value})
    return {"access_token": token, "token_type": "bearer"}

def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = repo.buscar_por_id(user_id, db)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario

def criar_usuario(nome: str, email: str, senha: str, perfil: PerfilUsuario, db: Session) -> Usuario:
    if repo.buscar_por_email(email, db):
        raise HTTPException(400, "E-mail já cadastrado")
    novo = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha),
        perfil=perfil,
    )
    return repo.salvar_usuario(novo, db)