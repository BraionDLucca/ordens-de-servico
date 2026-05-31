from fastapi import FastAPI
from core.database import engine, Base
import models

# Cria as tabelas no banco de dados SQLite caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Controle de Peças - Assistência Técnica",
    description="Módulo de gestão de inventário, histórico de movimentações e vínculo com Ordens de Serviço.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "modulo": "Controle de Peças",
        "mensagem": "A API está pronta para receber os endpoints de CRUD e regras de negócio."
    }