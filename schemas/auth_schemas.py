# schemas/auth_schemas.py
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UsuarioCreate(BaseModel):
    nome:  str
    email: str
    senha: str
    perfil: str  # "ADMIN", "TECNICO" ou "ATENDENTE"
    
class UsuarioResponse(BaseModel):
    id:     int
    nome:   str
    email:  str
    perfil: str
    class Config:
        from_attributes = True